def online_max(stream):
    # state=(count, current_max); memory O(1); input discarded after update
    count = 0
    current_max = None
    malformed = 0
    for raw in stream:                         # exactly once, left to right
        try:
            value = float(raw)
        except (TypeError, ValueError):
            malformed += 1                     # explicit policy: skip and count
            continue
        if not (value == value):               # NaN check
            malformed += 1
            continue
        count += 1
        if count == 1:
            current_max = value
        else:
            if value > current_max:
                current_max = value
    if count == 0:
        return {"count": 0, "malformed": malformed, "max": None}
    return {"count": count, "malformed": malformed, "max": current_max}

print(online_max(iter(["2", "4", "bad", "nan", "6"])))
print(online_max(iter([])))              # explicit end-of-stream behavior