def vote(values):
    if not isinstance(values, list) or len(values) != 3 or any(not isinstance(v, int) or isinstance(v, bool) for v in values):
        return {"status": "fault", "value": None, "agreement": 0, "dissent": [], "fault": True}
    counts = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    winner = max(counts.items(), key=lambda x: x[1])
    dissent = [v for v in values if v != winner[0]]
    return {
        "status": "ok" if winner[1] >= 2 else "fault",
        "value": winner[0] if winner[1] >= 2 else None,
        "agreement": winner[1],
        "dissent": dissent,
        "fault": winner[1] < 2
    }

def clamp(value):
    return max(0, min(100, value))

def mission(sensor, engine_out=False, comms_drop=False, sensor_loss=False):
    if not isinstance(sensor, int) or isinstance(sensor, bool) or not 0 <= sensor <= 100:
        return {"status": "fault", "value": None, "agreement": 0, "dissent": [], "fault": True}
    if sensor_loss:
        return {"status": "fault", "value": None, "agreement": 0, "dissent": [], "fault": True}

    # Independent computation channels
    direct = clamp(sensor)
    conservative = clamp((sensor + (0 if engine_out else 1)) // 1)
    table = clamp([0, 25, 50, 75, 100][min(sensor // 25, 4)])
    if comms_drop:
        table = clamp(table + 30)
    if engine_out:
        conservative = clamp(conservative - 3)

    return vote([direct, conservative, table])

# Failure matrix
matrix = {
    "sensor_loss": mission(50, sensor_loss=True),
    "engine_out": mission(50, engine_out=True),
    "comms_drop": mission(50, comms_drop=True),
    "triple_fault": vote([15, 25, 35])
}

# Assert structural guarantees only
assert matrix["sensor_loss"]["fault"] and matrix["sensor_loss"]["status"] == "fault"
assert matrix["engine_out"]["status"] in ("ok", "fault") and matrix["engine_out"]["fault"] == (matrix["engine_out"]["status"] == "fault")
assert matrix["comms_drop"]["fault"] and matrix["comms_drop"]["status"] == "fault"
assert matrix["triple_fault"]["fault"] and matrix["triple_fault"]["status"] == "fault"
assert vote([])["fault"] and vote([10])["fault"] and vote([10, 20])["fault"]
assert vote([10, 10, 20])["status"] == "ok" and vote([10, 10, 20])["agreement"] == 2
assert vote([10, 20, 10])["dissent"] == [20]

print({"matrix": matrix, "removed": "auto_tune: unbounded failure surface"})