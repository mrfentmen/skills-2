def decide(value, running_high):
    if value > running_high:
        return "BUY", "value > running_high"
    return "HOLD", "value <= running_high"

stream = [105, 95, 110, 100, 120]
running_high = float("-inf")
for item in stream:
    decision, rule = decide(item, running_high)
    print(f"{item}: {decision} ({rule})")
    if item > running_high:
        running_high = item