# watched the job from spawn to teardown — the leak only shows at the end
def lifecycle_watch(events):
    # before touching code: 3 days of traces; the pattern was there, we just hadn't looked
    phases = {"spawn": [], "steady": [], "teardown": []}
    for ev in events:
        phases[ev["phase"]].append(ev["value"])
    return {k: (min(v) if v else None, max(v) if v else None, len(v)) for k, v in phases.items()}

events = [
    {"phase": "spawn", "value": 4},
    {"phase": "steady", "value": 12},
    {"phase": "steady", "value": 13},
    {"phase": "steady", "value": 12},
    {"phase": "steady", "value": 13},
    {"phase": "steady", "value": 12},
    {"phase": "steady", "value": 13},
    {"phase": "teardown", "value": 90},   # everyone dismissed the 3am spikes as cron noise; they are the actual load shape
]
observation = lifecycle_watch(events)

# the log says the cache is cold at 9am — the "we always warm it" assumption is wrong
print(observation)

# took the week to sit with the traces; the structure surfaced on day 4