import json

def apply(state, event):
    if event["type"] == "add":
        return {"total": state["total"] + event["value"]}
    raise ValueError("unknown event")

def artifact(events):
    return {"schema": 1, "sequence": len(events), "events": json.loads(json.dumps(events))}

def recover(saved):
    if saved.get("schema") != 1 or saved.get("sequence") != len(saved.get("events", [])):
        raise ValueError("torn or unsupported artifact")
    state = {"total": 0}
    for event in saved["events"]:
        state = apply(state, event)
    return state, saved["sequence"]

events = [{"type": "add", "value": 5}, {"type": "add", "value": 7}, {"type": "add", "value": 2}]
live = {"total": 0}
for event in events:
    live = apply(live, event)
expected = dict(live)
saved = artifact(events)
live = None
reborn, position = recover(saved)
assert reborn == expected and position == len(events)
reborn = apply(reborn, {"type": "add", "value": 4})
assert reborn == {"total": 18}
try:
    recover({"schema": 1, "sequence": 3, "events": events[:2]})
except ValueError as exc:
    assert str(exc) == "torn or unsupported artifact"
else:
    raise AssertionError("torn artifact was accepted")
print({"state": reborn, "position": position + 1})