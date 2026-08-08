def vote(values):
    if not isinstance(values, list) or len(values) != 3 or any(not isinstance(v, int) or isinstance(v, bool) for v in values):
        return {"status": "fault", "value": None, "agreement": 0, "dissent": [], "fault": True}
    counts = {v: values.count(v) for v in values}
    winner, agreement = max(counts.items(), key=lambda pair: pair[1])
    dissent = [v for v in values if v != winner]
    return {
        "status": "ok" if agreement >= 2 else "fault",
        "value": winner if agreement >= 2 else None,
        "agreement": agreement,
        "dissent": dissent,
        "fault": agreement < 2
    }

def clamp(value):
    return max(0, min(100, value))

def mission_altitude(sensor, engine_out=False, comms_drop=False, sensor_loss=False):
    if not isinstance(sensor, int) or isinstance(sensor, bool) or not 0 <= sensor <= 100:
        return {"status": "fault", "value": None, "agreement": 0, "dissent": [], "fault": True}
    if sensor_loss:
        return {"status": "fault", "value": None, "agreement": 0, "dissent": [], "fault": True}

    # Independent computation paths:
    # 1. Direct sensor reading (raw telemetry)
    direct = clamp(sensor)

    # 2. Conservative average with engine-out compensation
    base = sensor
    if engine_out:
        base = max(0, base - 5)
    average = clamp((base + (base + 2)) // 2)

    # 3. Bounded table lookup with comms drop compensation
    table = [0, 15, 30, 45, 60, 75, 90, 100]
    lookup = clamp(table[sensor // 15])
    if comms_drop:
        lookup = clamp(lookup + 10)

    return vote([direct, average, lookup])

# Failure matrix scenarios
matrix = {
    "sensor_loss": mission_altitude(50, sensor_loss=True),
    "engine_out": mission_altitude(50, engine_out=True),
    "comms_drop": mission_altitude(50, comms_drop=True),
    "triple_fault": vote([10, 20, 30]),
    "nominal": mission_altitude(50)
}

# Assertions for failure matrix outcomes
assert matrix["sensor_loss"]["status"] == "fault" and matrix["sensor_loss"]["fault"]
assert matrix["engine_out"]["status"] == "ok" and matrix["engine_out"]["dissent"] == [47]
assert matrix["comms_drop"]["status"] == "ok" and matrix["comms_drop"]["dissent"] == [60]
assert matrix["triple_fault"]["status"] == "fault" and matrix["triple_fault"]["fault"]
assert matrix["nominal"]["status"] == "ok" and matrix["nominal"]["agreement"] == 3
assert vote([])["fault"] and mission_altitude("bad")["fault"]

# Removed feature: dynamic averaging window
# Reason: Adds unbounded state space to a fixed mission envelope; increases failure surface
# without measurable mission value for altitude computation in this bounded scenario.
print({"matrix": matrix, "removed": "dynamic_averaging_window: unbounded state space"})