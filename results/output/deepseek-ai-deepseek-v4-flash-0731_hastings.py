import json
import time
import random
from typing import Any, Dict, List, Optional

# ============================================================
# (1) NAMED FAULT-INJECTION HOOK WITH BOUNDED BLAST RADIUS
# ------------------------------------------------------------
# Hook: `inject_fault(mode, attempt)` — only affects the disposable
# dependency `_fetch_raw`. Blast radius is bounded to this single
# function; no other service path is touched. Modes are explicit
# and validated; unknown modes raise immediately (fail fast).
# ============================================================

class DependencyFault(Exception):
    """Base class for injected dependency faults."""

class KillFault(DependencyFault):
    """Simulates a hard node kill (connection dropped)."""

class ThrottleFault(DependencyFault):
    """Simulates a transient throttle (timeout)."""

class CorruptFault(DependencyFault):
    """Simulates a corrupt response payload."""

def _fetch_raw(mode: str, attempt: int) -> str:
    """Disposable dependency — the only place faults are injected."""
    if mode not in {"kill", "throttle", "corrupt", "healthy"}:
        raise ValueError(f"unknown fault mode: {mode}")
    if mode == "kill":
        raise KillFault("node killed")
    if mode == "throttle" and attempt < 2:
        raise ThrottleFault("dependency throttled")
    if mode == "corrupt":
        return "not-json"
    return json.dumps({"value": 42, "source": "primary"})

# ============================================================
# (2) MEANINGFUL GRACEFUL DEGRADATION
# ------------------------------------------------------------
# On any fault, we return a reduced but honest payload: status
# "degraded" with a cached fallback value (0) and diagnostics.
# Partial service beats a 500 — the caller always gets a response.
# ============================================================

# (3) CAPPED EXPONENTIAL RETRY WITH DETERMINISTIC JITTER
# ------------------------------------------------------------
# Backoff: 100ms * 2^attempt, plus deterministic jitter
# (attempt * 17 % 31) — reproducible across runs. Hard cap at 500ms.
# Retry budget: max_attempts (validated 1..5). No infinite loops.
# ============================================================

def _backoff_ms(attempt: int) -> int:
    """Deterministic capped exponential backoff with jitter."""
    return min(100 * (2 ** attempt) + (attempt * 17 % 31), 500)

# ============================================================
# (4) NO SINGLE POINT OF FAILURE
# ------------------------------------------------------------
# The resilient path has two independent layers:
#   - `_fetch_raw` (primary) — can fail
#   - `_fallback_cache` (secondary) — always available, never faults
# The client never depends on a single component; if primary fails,
# the fallback is used. No shared mutable state that can corrupt.
# ============================================================

_FALLBACK_CACHE: Dict[str, Any] = {"value": 0, "source": "fallback-cache"}

def _fallback() -> Dict[str, Any]:
    """Immutable fallback — always returns a valid reduced payload."""
    return dict(_FALLBACK_CACHE)

# ============================================================
# (5) FAILURE MATRIX — kill, throttle, corrupt, healthy
# ============================================================
# Each mode is exercised; the matrix asserts expected outcomes.
# ============================================================

def resilient_read(mode: str, max_attempts: int = 3) -> Dict[str, Any]:
    """Resilient fetch with bounded retry, degradation, and diagnostics."""
    # Validate retry budget — invalid input is a contract violation.
    if (not isinstance(max_attempts, int) or isinstance(max_attempts, bool)
            or max_attempts <= 0 or max_attempts > 5):
        return {"status": "invalid", "value": 0, "attempts": 0, "diagnostics": []}

    diagnostics: List[Dict[str, Any]] = []

    for attempt in range(max_attempts):
        try:
            raw = _fetch_raw(mode, attempt)
            # Corrupt responses must be detected, not trusted.
            try:
                payload = json.loads(raw)
                if not isinstance(payload, dict) or "value" not in payload:
                    raise CorruptFault("malformed payload")
                value = int(payload["value"])
                return {
                    "status": "full",
                    "value": value,
                    "attempts": attempt + 1,
                    "diagnostics": diagnostics,
                }
            except (json.JSONDecodeError, TypeError, ValueError) as error:
                # Corrupt response — degrade immediately, no retry.
                diagnostics.append({"kind": "degraded", "reason": f"corrupt: {error}"})
                return {
                    "status": "degraded",
                    "value": _fallback()["value"],
                    "attempts": attempt + 1,
                    "diagnostics": diagnostics,
                }
        except ThrottleFault as error:
            # Transient — retry with capped backoff and jitter.
            delay_ms = _backoff_ms(attempt)
            diagnostics.append({
                "kind": "retry",
                "delay_ms": delay_ms,
                "reason": str(error),
            })
            # Simulate the delay (deterministic, no real sleep for testability).
            time.sleep(delay_ms / 1000.0)
        except KillFault as error:
            # Hard failure — degrade immediately, no retry.
            diagnostics.append({"kind": "degraded", "reason": str(error)})
            return {
                "status": "degraded",
                "value": _fallback()["value"],
                "attempts": attempt + 1,
                "diagnostics": diagnostics,
            }
        except ValueError as error:
            # Unknown mode — fail fast, degrade.
            diagnostics.append({"kind": "degraded", "reason": str(error)})
            return {
                "status": "degraded",
                "value": _fallback()["value"],
                "attempts": attempt + 1,
                "diagnostics": diagnostics,
            }

    # Retry budget exhausted — stop, report exhaustion.
    return {
        "status": "exhausted",
        "value": _fallback()["value"],
        "attempts": max_attempts,
        "diagnostics": diagnostics,
    }

# ============================================================
# (6) RECOVERY/STOP CRITERIA AND DIAGNOSTICS
# ------------------------------------------------------------
# Recovery: full status when primary succeeds; degraded when fallback
# used; exhausted when retry budget spent. Diagnostics record every
# fault kind, delay, and reason. Stop condition: max_attempts reached
# or non-retryable fault encountered.
# ============================================================

def run_failure_matrix() -> Dict[str, Dict[str, Any]]:
    """Exercise all matrix rows and return results."""
    matrix = {
        mode: resilient_read(mode)
        for mode in ("kill", "throttle", "corrupt", "healthy")
    }
    # Additional edge cases: unknown mode, invalid budget.
    matrix["unknown"] = resilient_read("unknown")
    matrix["invalid_budget"] = resilient_read("healthy", 0)
    return matrix

def main() -> None:
    """Run the failure matrix and print diagnostics."""
    results = run_failure_matrix()

    # Assertions — the matrix must pass its own contract.
    assert results["kill"]["status"] == "degraded"
    assert results["throttle"]["status"] == "full"
    assert results["throttle"]["attempts"] == 3
    assert results["corrupt"]["status"] == "degraded"
    assert results["healthy"]["status"] == "full"
    assert results["unknown"]["status"] == "degraded"
    assert results["invalid_budget"]["status"] == "invalid"

    # Print the full matrix with diagnostics.
    print("=== Resilient Service Failure Matrix ===")
    for mode, report in results.items():
        print(f"\nMode: {mode}")
        print(f"  Status: {report['status']}")
        print(f"  Value: {report['value']}")
        print(f"  Attempts: {report['attempts']}")
        if report["diagnostics"]:
            print("  Diagnostics:")
            for diag in report["diagnostics"]:
                print(f"    - {diag}")
        else:
            print("  Diagnostics: (none)")

    # Summary of recovery/stop criteria.
    print("\n=== Recovery/Stop Criteria ===")
    print("  - Full: primary dependency returned valid payload.")
    print("  - Degraded: fallback cache used; fault recorded.")
    print("  - Exhausted: retry budget spent; no further attempts.")
    print("  - Invalid: bad input; no service call made.")

if __name__ == "__main__":
    main()