import math

def parse_measurements(raw_values):
    # Input contract: raw_values must be a list of numeric strings or numbers.
    # Accepted range: finite numbers in [-1000.0, 1000.0].
    # Boundary checks: reject bool, non-finite, out-of-range, non-numeric strings.
    if not isinstance(raw_values, list):
        return {"status": "rejected", "reason": "expected list", "accepted": 0, "rejected": 1}
    if len(raw_values) > 1000:
        return {"status": "rejected", "reason": "list too large", "accepted": 0, "rejected": len(raw_values)}

    accepted = []
    rejected = 0
    for raw in raw_values:
        # Malformed input: wrong type, non-finite, out-of-range, or unparseable string
        if isinstance(raw, bool):
            rejected += 1
            continue
        if isinstance(raw, (int, float)):
            value = float(raw)
            if not math.isfinite(value) or not -1000.0 <= value <= 1000.0:
                rejected += 1
                continue
            accepted.append(value)
        elif isinstance(raw, str):
            try:
                value = float(raw)
            except (ValueError, TypeError):
                rejected += 1
                continue
            if not math.isfinite(value) or not -1000.0 <= value <= 1000.0:
                rejected += 1
                continue
            accepted.append(value)
        else:
            # Unexpected state: unsupported type
            rejected += 1
            continue

    if not accepted:
        return {"status": "unavailable", "reason": "no valid measurements", "accepted": 0, "rejected": rejected}

    # Safe fallback: return valid partial results with explicit validity scope
    return {
        "status": "ok",
        "mean": sum(accepted) / len(accepted),
        "min": min(accepted),
        "max": max(accepted),
        "accepted": len(accepted),
        "rejected": rejected,
    }

# Tests: valid, boundary, malformed, and unexpected state
valid_result = parse_measurements([10, 20, "30.5", -1000.0, 1000.0])
assert valid_result["status"] == "ok"
assert valid_result["mean"] == 12.1
assert valid_result["accepted"] == 5
assert valid_result["rejected"] == 0

boundary_result = parse_measurements([-1000.0, 1000.0, 0])
assert boundary_result["status"] == "ok"
assert boundary_result["accepted"] == 3
assert boundary_result["rejected"] == 0

malformed_result = parse_measurements([10, "bad", True, float("nan"), 2000, None])
assert malformed_result["status"] == "ok"
assert malformed_result["accepted"] == 1
assert malformed_result["rejected"] == 5

unavailable_result = parse_measurements(["bad", True, None])
assert unavailable_result["status"] == "unavailable"
assert unavailable_result["accepted"] == 0
assert unavailable_result["rejected"] == 3

rejected_result = parse_measurements("not a list")
assert rejected_result["status"] == "rejected"
assert rejected_result["rejected"] == 1

print("valid:", valid_result)
print("boundary:", boundary_result)
print("malformed:", malformed_result)
print("unavailable:", unavailable_result)
print("rejected:", rejected_result)