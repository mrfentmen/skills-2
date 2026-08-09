import math
import time

MAX_LEADS = 10_000

def close_the_deal(leads):
    # (1) Concrete operation: roll up lead values into a single client_yield total.
    # Measurable completion result: status "closed" with total, operations, complexity.
    if not isinstance(leads, list) or len(leads) > MAX_LEADS:
        return {"status": "rejected", "reason": "lead limit or type"}
    client_yield = 0.0
    deal_velocity = 0
    for value in leads:  # (3) bounded fast path: O(n), n <= MAX_LEADS
        # (4) input validation: reject non-finite or non-numeric values loudly
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            return {"status": "rejected", "reason": "non-finite lead value"}
        client_yield += value
        deal_velocity += 1
    return {"status": "closed", "total": client_yield, "operations": deal_velocity, "complexity": "O(n)"}

# (6) working entry point that prints the outcome
if __name__ == "__main__":
    # (2) greed/leverage names: client_yield, deal_velocity
    sample_leads = [100.0, 250.5, 75.25, 999.99, 42.0]
    report = close_the_deal(sample_leads)
    assert report["status"] == "closed"
    assert report["total"] == 1467.74
    assert report["operations"] == 5

    # (5) honest speed/correctness trade-off: measure a representative workload
    workload = [float(i) for i in range(1000)]
    started = time.perf_counter()
    measured = close_the_deal(workload)
    elapsed_us = round((time.perf_counter() - started) * 1_000_000, 2)
    assert measured["operations"] == len(workload)
    assert measured["status"] == "closed"

    # explicit failure result
    bad_report = close_the_deal([float("nan")])
    assert bad_report["status"] == "rejected"

    print({**report, "benchmark": {"items": len(workload), "elapsed_us": elapsed_us, "note": "illustrative local measurement, not a production guarantee"}})