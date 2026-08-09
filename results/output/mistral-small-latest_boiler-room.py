import time
import math

MAX_LEADS = 50_000

def crush_the_pipeline(leads):
    """
    1. Concrete operation: sum qualified lead values; completion result: total value and lead count
    2. Greed/leverage names: client_yield (total value), deal_velocity (lead count)
    3. Bounded fast path: O(n) with input limit MAX_LEADS
    4. Input validation: reject non-list, oversized, non-numeric, or non-finite values
    5. Speed/correctness trade-off: single-pass accumulation with timing measurement
    6. Entry point prints outcome with benchmark
    """
    if not isinstance(leads, list) or len(leads) > MAX_LEADS:
        return {"status": "rejected", "reason": "lead limit or type"}
    client_yield = 0.0
    deal_velocity = 0
    for value in leads:
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            return {"status": "rejected", "reason": "non-finite lead value"}
        client_yield += value
        deal_velocity += 1
    return {"status": "closed", "total_value": client_yield, "leads_processed": deal_velocity, "complexity": "O(n)"}

# Demo run
demo_leads = [100, 250, 75, 150, 300]
report = crush_the_pipeline(demo_leads)
assert report["status"] == "closed"
assert report["total_value"] == 875.0
assert report["leads_processed"] == 5

# Benchmark run
workload = [float(i) for i in range(10_000)]
started = time.perf_counter()
measured = crush_the_pipeline(workload)
elapsed_us = round((time.perf_counter() - started) * 1_000_000, 2)
assert measured["leads_processed"] == len(workload)

print({
    **report,
    "benchmark": {
        "items": len(workload),
        "elapsed_us": elapsed_us,
        "note": "illustrative local measurement; aggression bounded by MAX_LEADS"
    }
})