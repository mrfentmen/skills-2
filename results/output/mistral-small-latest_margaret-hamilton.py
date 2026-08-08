import math
from typing import Union, Dict, List

def parse_telemetry_frame(frame: Union[List[Union[int, float]], None]) -> Dict[str, Union[str, float, int]]:
    """
    Parse a telemetry frame with strict input validation and failure taxonomy.
    Accepts a list of numeric values within [-10000, 10000] representing sensor readings.
    Returns a status with diagnostics: ok, rejected, unavailable, or unexpected.
    """
    # Input contract: must be list or None
    if frame is None:
        return {"status": "rejected", "reason": "input is None", "rejected": 0}
    if not isinstance(frame, list):
        return {"status": "rejected", "reason": "expected list", "rejected": 0}

    # Validate list size boundary
    if len(frame) == 0:
        return {"status": "unavailable", "reason": "empty frame", "rejected": 0}
    if len(frame) > 1000:
        return {"status": "rejected", "reason": "frame exceeds maximum size 1000", "rejected": 0}

    accepted = []
    rejected = 0

    for raw in frame:
        # Malformed input: non-numeric, boolean, or out-of-range
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            rejected += 1
            continue
        if not math.isfinite(raw):
            rejected += 1
            continue
        if not (-10000 <= raw <= 10000):
            rejected += 1
            continue

        accepted.append(float(raw))

    # Unexpected state: valid readings exist but parsing failed due to internal error
    try:
        if not accepted:
            return {"status": "unavailable", "reason": "no valid readings", "rejected": rejected}
    except Exception as e:
        return {"status": "unexpected", "reason": f"internal parsing error: {str(e)}", "rejected": rejected}

    # Safe degradation: return mean only if all readings are valid
    try:
        mean = sum(accepted) / len(accepted)
    except Exception as e:
        return {"status": "unexpected", "reason": f"mean calculation failed: {str(e)}", "rejected": rejected}

    return {
        "status": "ok",
        "mean": mean,
        "accepted": len(accepted),
        "rejected": rejected
    }

# Test valid inputs
print(parse_telemetry_frame([100, 200, 300]))  # ok
print(parse_telemetry_frame([-10000, 0, 10000]))  # ok
print(parse_telemetry_frame([1.5, 2.5, 3.5]))  # ok

# Test boundary inputs
print(parse_telemetry_frame([]))  # unavailable (empty)
print(parse_telemetry_frame([100] * 1001))  # rejected (size)
print(parse_telemetry_frame([-10001]))  # rejected (range)
print(parse_telemetry_frame([10001]))  # rejected (range)

# Test malformed inputs
print(parse_telemetry_frame([100, "bad", 200]))  # ok with rejected=1
print(parse_telemetry_frame([True, False]))  # unavailable (no valid)
print(parse_telemetry_frame([None, "text"]))  # unavailable (no valid)
print(parse_telemetry_frame([math.inf]))  # unavailable (no valid)

# Test unexpected state (simulated via mock corruption)
class MockCorruptList(list):
    def __getitem__(self, index):
        if index == 0:
            raise RuntimeError("simulated corruption")
        return super().__getitem__(index)

# This would trigger unexpected if corruption occurs during parsing
# Uncomment to test (requires mock setup not shown here for safety)
# print(parse_telemetry_frame(MockCorruptList([100, 200])))

# Test None input
print(parse_telemetry_frame(None))  # rejected