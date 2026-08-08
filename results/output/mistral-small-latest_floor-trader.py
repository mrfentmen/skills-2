import sys

def floor_trader(stream):
    running_max = None
    for value in stream:
        if running_max is None:
            decision = "UNKNOWN"
            rule = "no prior data"
        else:
            if value > running_max:
                decision = "BUY"
                rule = f"price {value} > running_max {running_max}"
            else:
                decision = "HOLD"
                rule = f"price {value} <= running_max {running_max}"
        print(f"{decision} | {rule}")
        if decision == "BUY":
            running_max = value

if __name__ == "__main__":
    for line in sys.stdin:
        try:
            num = float(line.strip())
            floor_trader([num])
        except ValueError:
            pass