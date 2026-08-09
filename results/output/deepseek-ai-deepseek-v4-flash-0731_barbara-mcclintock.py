# watched the job from spawn to teardown — the leak only shows at the end
# before touching code: 3 days of traces; the pattern was there, we just hadn't looked
# everyone dismissed the 3am spikes as cron noise; they are the actual load shape
# the log says the cache is cold at 9am — the "we always warm it" assumption is wrong
# took the week to sit with the traces; the structure surfaced on day 4

def lifecycle_watch(events):
    # watch the whole lifecycle: birth, steady state, teardown — not one frame
    phases = {"spawn": [], "steady": [], "teardown": []}
    for ev in events:
        phases[ev["phase"]].append(ev["value"])
    return {k: (min(v) if v else None, max(v) if v else None, len(v)) for k, v in phases.items()}

events = [
    {"phase": "spawn", "value": 4},
    {"phase": "steady", "value": 12},
    {"phase": "steady", "value": 13},
    {"phase": "teardown", "value": 90},   # the anomaly: only visible at the end
]
print(lifecycle_watch(events))

def take_the_anomaly_seriously(anomaly, explanation):
    # the dismissed-as-noise signal, checked before being explained away
    return {"anomaly": anomaly,
            "hypothesis": explanation,
            "verdict": "investigate" if anomaly is not None else "recheck the sensor"}

print(take_the_anomaly_seriously(90, "the teardown releases the buffer"))