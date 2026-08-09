import json
from typing import List, Dict, Any

def apply(state: Dict[str, Any], event: Dict[str, Any]) -> Dict[str, Any]:
    if event["type"] == "add":
        return {"sum": state["sum"] + event["value"]}
    raise ValueError("unknown event type")

def artifact(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema": 1,
        "sequence": len(events),
        "events": json.loads(json.dumps(events))
    }

def recover(saved: Dict[str, Any]) -> Dict[str, Any]:
    if saved.get("schema") != 1 or saved.get("sequence") != len(saved.get("events", [])):
        raise ValueError("torn or unsupported artifact")
    state = {"sum": 0}
    for event in saved["events"]:
        state = apply(state, event)
    return state

events = [{"type": "add", "value": 5}, {"type": "add", "value": 3}, {"type": "add", "value": 2}]
live = {"sum": 0}
for event in events:
    live = apply(live, event)
expected = dict(live)
saved = artifact(events)
live = None  # active state dies
reborn = recover(saved)  # resurrect from artifact
assert reborn == expected, "recovered state does not match expected"
reborn = apply(reborn, {"type": "add", "value": 4})
assert reborn == {"sum": 14}, "continuation after recovery failed"
try:
    recover({"schema": 1, "sequence": 3, "events": events[:2]})
except ValueError as exc:
    assert str(exc) == "torn or unsupported artifact"
else:
    raise AssertionError("torn artifact was accepted")
print({"state": reborn, "position": 4})