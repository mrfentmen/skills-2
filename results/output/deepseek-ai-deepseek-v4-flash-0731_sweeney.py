import time

BUDGET_MS = 16.6
MAX_ENTITIES = 10_000

def process_batch(entities, quality="full"):
    if (not isinstance(entities, list) or len(entities) > MAX_ENTITIES
            or any(not isinstance(e, int) or isinstance(e, bool) for e in entities)
            or quality not in {"full", "degraded"}):
        return {"status": "rejected", "reason": "unsupported workload or quality"}

    start = time.perf_counter()
    # contiguous data-oriented pass: single linear scan, no allocation
    processed = 0
    for e in entities:
        if e % 2 == 0:
            processed += 1
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    work_units = len(entities)
    # smoke-model cost estimate (not hardware proof); wall-clock above is the real gate
    cost_ms = work_units * (0.1 if quality == "full" else 0.04)

    if cost_ms > BUDGET_MS and quality == "full":
        return process_batch(entities, quality="degraded")

    status = "full" if quality == "full" else "degraded"
    if elapsed_ms > BUDGET_MS:
        status = "rejected"

    return {
        "status": status,
        "cost_ms": cost_ms,
        "wall_clock_ms": elapsed_ms,
        "work_units": work_units,
        "processed": processed,
        "entities": len(entities),
        "format": "entity-batch-v1-json",
        "budget_ms": BUDGET_MS,
    }

largest_scene = list(range(150))
report = process_batch(largest_scene)
assert report["status"] == "full" and report["cost_ms"] == 15.0 and report["work_units"] == 150 and report["processed"] == 75
assert process_batch(list(range(200)), "full")["status"] == "degraded"
assert process_batch(list(range(10)), "unknown")["status"] == "rejected"
assert process_batch([1, "bad"], "full")["status"] == "rejected"
assert report["format"] == "entity-batch-v1-json"
print(report)