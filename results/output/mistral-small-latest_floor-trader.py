import sys

def floor_trader_stream(stream):
    running_max = None
    for value in stream:
        if running_max is None:
            decision = "HOLD"
            rule = "no prior value to compare"
        else:
            if value > running_max:
                decision = "BUY"
                rule = f"price {value} exceeds running max {running_max}"
            else:
                decision = "HOLD"
                rule = f"price {value} does not exceed running max {running_max}"
        print(f"{decision} | {rule}")
        if decision == "BUY":
            running_max = value

if __name__ == "__main__":
    for line in sys.stdin:
        try:
            num = float(line.strip())
            floor_trader_stream([num])
        except ValueError:
            pass