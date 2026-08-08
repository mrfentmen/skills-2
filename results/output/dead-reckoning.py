def online_max(stream):
    # state=(count, max_value, malformed); memory O(1); input discarded after update
    count = 0
    max_value = None
    malformed = 0
    for raw in stream:                         # exactly once, left to right
        try:
            value = float(raw)
        except (TypeError, ValueError):
            malformed += 1                     # explicit policy: skip and count
            continue
        if not math.isfinite(value):
            malformed += 1                     # reject NaN and infinity
            continue
        count += 1
        if max_value is None or value > max_value:
            max_value = value
    # empty -> None; nonempty -> max, count, malformed
    return {"count": count, "malformed": malformed, "max": max_value}

import math
print(online_max(iter(["2", "4", "bad", "nan", "6"])))
print(online_max(iter([])))              # explicit end-of-stream behavior