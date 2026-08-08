import sys

def ritual(armed=False):
    # Named disposable resource, owner, precondition, and trade rationale
    resource = {"owner": "ritual", "token": "arcane", "payload": [i for i in range(100)]}
    plan = {
        "owner": "ritual function",
        "target": "in-memory token cache",
        "trade": "release token to free memory before computing checksum",
        "precondition": "owner == 'ritual' and 'token' in resource"
    }

    # Dry-run default: inspect without mutation
    if not armed:
        return {
            "status": "dry-run",
            "plan": plan,
            "resource_present": resource.get("owner") == "ritual" and "token" in resource,
            "sacrificed": False,
            "result": None
        }

    # Precondition before spell: verify exact expected state
    if resource.get("owner") != "ritual" or "token" not in resource:
        raise RuntimeError("sacrifice precondition failed: unexpected resource state")

    # Sacrifice before the main algorithm
    del resource["token"]

    # Post-sacrifice verification
    if "token" in resource:
        raise RuntimeError("sacrifice was not verified: token still present")

    # Real computation after sacrifice
    result = sum(resource["payload"]) * 2  # checksum of remaining data

    return {
        "status": "armed",
        "plan": plan,
        "resource_present": False,
        "sacrificed": True,
        "result": result
    }

report = ritual("--arm-sacrifice" in sys.argv)
assert report["status"] in {"dry-run", "armed"}
if report["status"] == "armed":
    assert report["sacrificed"] and report["result"] == 9900
print(report)