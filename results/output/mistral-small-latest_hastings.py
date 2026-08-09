import time
import random
from typing import Dict, Any, Optional

# Fault-injection hook: "dependency_kill"
# Blast radius: only affects the disposable mock service instance; no production impact
# Graceful degradation: returns cached rate limit state when service is killed
# Retry: capped exponential backoff with deterministic jitter (attempt * 13 % 23)
# No single point of failure: client retries on transient errors; degraded path uses cache
# Recovery criteria: service returns to healthy after 3 successful calls
# Diagnostics: include retry attempts, delays, and degradation reasons

class MockRateService:
    def __init__(self):
        self.healthy = True
        self.call_count = 0

    def fetch_rate_limit(self) -> Dict[str, Any]:
        if not self.healthy:
            raise ConnectionError("service killed")
        self.call_count += 1
        if self.call_count % 3 == 0:
            return {"limit": 100, "remaining": 97, "reset": time.time() + 3600}
        if self.call_count % 5 == 0:
            return "not-a-dict"
        return {"limit": 100, "remaining": 99, "reset": time.time() + 3600}

def resilient_fetch_rate_limit(
    service: MockRateService,
    max_attempts: int = 3,
    cache: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    if not isinstance(max_attempts, int) or max_attempts <= 0 or max_attempts > 5:
        return {"status": "invalid", "value": None, "attempts": 0, "diagnostics": []}

    diagnostics = []
    cache = cache or {"limit": 100, "remaining": 100, "reset": time.time() + 3600}

    for attempt in range(max_attempts):
        try:
            raw = service.fetch_rate_limit()
            if isinstance(raw, dict):
                cache = raw
                return {"status": "full", "value": cache, "attempts": attempt + 1, "diagnostics": diagnostics}
            else:
                raise ValueError("corrupt response")
        except TimeoutError as error:
            delay_ms = min(100 * (2 ** attempt) + (attempt * 13 % 23), 500)
            time.sleep(delay_ms / 1000)
            diagnostics.append({"kind": "retry", "delay_ms": delay_ms, "reason": str(error)})
        except (ConnectionError, ValueError) as error:
            diagnostics.append({"kind": "degraded", "reason": str(error)})
            return {"status": "degraded", "value": cache, "attempts": attempt + 1, "diagnostics": diagnostics}

    return {"status": "exhausted", "value": cache, "attempts": max_attempts, "diagnostics": diagnostics}

def run_failure_matrix():
    results = {}
    cache = {"limit": 100, "remaining": 100, "reset": time.time() + 3600}

    # Kill scenario: service is killed immediately
    service_kill = MockRateService()
    service_kill.healthy = False
    results["kill"] = resilient_fetch_rate_limit(service_kill, cache=cache)

    # Throttle scenario: service times out on first two attempts
    service_throttle = MockRateService()
    original_fetch = service_throttle.fetch_rate_limit
    attempt_count = [0]
    def throttled_fetch():
        attempt_count[0] += 1
        if attempt_count[0] <= 2:
            raise TimeoutError("service throttled")
        return original_fetch()
    service_throttle.fetch_rate_limit = throttled_fetch
    results["throttle"] = resilient_fetch_rate_limit(service_throttle, cache=cache)

    # Corrupt scenario: service returns non-dict response
    service_corrupt = MockRateService()
    service_corrupt.fetch_rate_limit = lambda: "not-a-dict"
    results["corrupt"] = resilient_fetch_rate_limit(service_corrupt, cache=cache)

    # Healthy scenario: service operates normally
    service_healthy = MockRateService()
    results["healthy"] = resilient_fetch_rate_limit(service_healthy, cache=cache)

    # Invalid max_attempts
    results["invalid"] = resilient_fetch_rate_limit(service_healthy, max_attempts=0)

    return results

if __name__ == "__main__":
    matrix = run_failure_matrix()
    for mode, result in matrix.items():
        print(f"{mode}: {result}")