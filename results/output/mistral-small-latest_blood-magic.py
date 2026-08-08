import sys

def blood_magic(armed=False):
    # Disposable resource: an in-memory cache owned by the program
    cache = {"owner": "blood-mage", "data": "sensitive_temp_value", "size": 1024}
    plan = {
        "owner": "this function",
        "target": "program-owned cache",
        "trade": "release exclusive access to cache by clearing its contents",
        "precondition": {"owner": "blood-mage", "data": "sensitive_temp_value", "size": 1024},
        "postcondition": {"owner": "blood-mage", "data": None, "size": 0}
    }

    # Dry-run: report the planned sacrifice without mutation
    if not armed:
        return {
            "status": "dry-run",
            "plan": plan,
            "cache_state": cache.copy(),
            "sacrifice_planned": "data" in cache and cache["data"] == "sensitive_temp_value"
        }

    # Pre-sacrifice verification: ensure the cache is in the expected state
    if cache.get("owner") != "blood-mage" or cache.get("data") != "sensitive_temp_value" or cache.get("size") != 1024:
        raise RuntimeError("sacrifice precondition failed: cache is not in expected state")

    # Sacrifice: release the resource by clearing its contents
    sacrificed_data = cache["data"]
    cache.clear()
    cache["owner"] = "blood-mage"  # Keep owner to maintain ownership ward
    cache["size"] = 0

    # Post-sacrifice verification: confirm the resource was released
    if cache.get("data") is not None or cache.get("size") != 0:
        raise RuntimeError("sacrifice verification failed: resource not properly released")

    # Main algorithm: compute the sum of squares up to 1000
    result = sum(i * i for i in range(1000))

    return {
        "status": "armed",
        "sacrificed": sacrificed_data,
        "result": result,
        "plan": plan
    }

# Default dry-run unless explicitly armed
armed = "--arm-sacrifice" in sys.argv
report = blood_magic(armed)

# Validate report structure
assert report["status"] in {"dry-run", "armed"}
if report["status"] == "armed":
    assert report["sacrificed"] == "sensitive_temp_value"
    assert report["result"] == sum(i * i for i in range(1000))

print(report)