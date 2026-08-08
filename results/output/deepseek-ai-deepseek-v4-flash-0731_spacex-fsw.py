def vote(strings):
    if not isinstance(strings, list) or len(strings) != 3 or any(not isinstance(value, int) or isinstance(value, bool) for value in strings):
        return {"status": "fault", "value": None, "agreement": 0, "dissent": [], "fault": True}
    counts = {value: strings.count(value) for value in strings}
    winner, agreement = max(counts.items(), key=lambda pair: pair[1])
    dissent = [value for value in strings if value != winner]
    return {"status": "ok" if agreement >= 2 else "fault", "value": winner if agreement >= 2 else None,
            "agreement": agreement, "dissent": dissent, "fault": agreement < 2}

def clamp(value):
    return max(0, min(100, value))

def mission(sensor, engine_out=False, comms_drop=False, sensor_loss=False):
    if not isinstance(sensor, int) or isinstance(sensor, bool) or not 0 <= sensor <= 100:
        return {"status": "fault", "value": None, "agreement": 0, "dissent": [], "fault": True}
    if sensor_loss:
        return {"status": "fault", "value": None, "agreement": 0, "dissent": [], "fault": True}
    # Independent strings: direct sensor, conservative average, and bounded table lookup.
    direct = clamp(sensor)
    average = clamp((sensor + (0 if engine_out else 2)) // 1)
    lookup = clamp([0, 20, 40, 60, 80, 100][sensor // 20])
    if comms_drop:
        lookup = clamp(lookup + 25)
    if engine_out:
        average = clamp(average - 2)
    return vote([direct, average, lookup])

matrix = {"sensor_loss": mission(40, sensor_loss=True), "engine_out": mission(40, engine_out=True), "comms_drop": mission(40, comms_drop=True), "triple_fault": vote([10, 20, 30])}
assert matrix["sensor_loss"]["status"] == "fault" and matrix["sensor_loss"]["fault"]
assert matrix["engine_out"]["status"] == "ok" and matrix["engine_out"]["dissent"] == [38]
assert matrix["comms_drop"]["status"] == "fault" and matrix["triple_fault"]["fault"]
assert vote([])["fault"] and mission("bad")["fault"]
print({"matrix": matrix, "removed": "auto_tune: unbounded failure surface"})