import random

# (1) Tail statement: worst realistic case
# A 10x demand spike on a 3-node pool with 99.99th percentile latency — 
# probability shape: power-law tail (Pareto, alpha ~1.5), not Gaussian.
# Expected loss if unmitigated: total outage, not degradation.

# (2) Barbell allocation
# Core: 90% of budget -> immutable, stateless, redundant services with circuit breakers, fail closed.
# Edge: 10% -> isolated canary with feature flags, can be killed without touching core.

# (3) Convexity move
# All retries are idempotent (POST with idempotency keys, jobs with unique run IDs).
# A double-run of any job is harmless; failures are local and cheap, successes scale automatically.

# (4) Via-negativa item
# Removed: the distributed caching layer (Redis) — it was the single point of failure,
# added latency, and masked stale data. The system is simpler and more robust without it.

# (5) Skin-in-the-game note
# The architect and on-call engineer are the same person. If the design fails at 3 a.m.,
# they get paged. No blame-shifting to "ops" or "the cloud."

def tail_statement():
    return {
        "worst_case": "10x traffic on 3-node pool",
        "probability_shape": "power-law (Pareto alpha=1.5), not Gaussian",
        "impact": "total outage, not graceful degradation",
        "mitigation": "circuit breakers + fail-closed core"
    }

def barbell_allocation():
    return {
        "core": "90% budget: immutable, redundant, stateless, fail-closed",
        "edge": "10% budget: isolated canary with feature flags",
        "middle": "0% — no moderate risk that can quietly ruin you"
    }

def convexity_move():
    return {
        "retries": "idempotent with exponential backoff + jitter",
        "double_run": "harmless (unique run IDs, idempotency keys)",
        "failure_scope": "local and cheap; successes scale automatically"
    }

def via_negativa():
    return {
        "removed": "distributed caching layer (Redis)",
        "why": "single point of failure, added latency, masked stale data",
        "result": "simpler, more robust, fewer moving parts"
    }

def skin_in_the_game():
    return {
        "who": "the architect and on-call engineer are the same person",
        "exposure": "paged at 3 a.m. when the design fails",
        "no_blame": "no shifting to ops or cloud provider"
    }

def main():
    print("=== Robust-Design Analysis (Taleb-style) ===")
    print("\n(1) Tail statement:")
    for k, v in tail_statement().items():
        print(f"  {k}: {v}")
    print("\n(2) Barbell allocation:")
    for k, v in barbell_allocation().items():
        print(f"  {k}: {v}")
    print("\n(3) Convexity move:")
    for k, v in convexity_move().items():
        print(f"  {k}: {v}")
    print("\n(4) Via negativa:")
    for k, v in via_negativa().items():
        print(f"  {k}: {v}")
    print("\n(5) Skin in the game:")
    for k, v in skin_in_the_game().items():
        print(f"  {k}: {v}")

    # Demonstrate convex retry with jitter
    delays = [min(2 ** i, 8) * (0.5 + random.random() / 2) for i in range(4)]
    print(f"\nConvex retry backoff (seconds, jittered): {delays}")

if __name__ == "__main__":
    main()