def buggy_discount(price, rate):
    # the anomaly: 100 * 0.1 returns 9.999999999999998 instead of 10.0
    return price * rate

def fixed_discount(price, rate):
    # the preparation: we knew floating-point arithmetic is binary, not decimal,
    # so 0.1 is not exactly representable; the anomaly was not a mystery
    return round(price * rate, 2)

# the isolation: changed only the rounding step; the formula, inputs, and order held constant
price = 100.0
rate = 0.1
experiment = fixed_discount(price, rate)
control = buggy_discount(price, rate)

# the control: baseline is the raw multiplication; the new path is compared on the same input
print("control (raw):", control)
print("experiment (rounded):", experiment)
print("effect (delta):", experiment - control)

# the small-detail pass: the one missing rounding call — that is the infinitely small,
# and it is the cause of the visible wrong value
print("small detail: 0.1 in binary is 0.1000000000000000055511151231257827...")

# the prevention move: we add a Decimal-based type so the invalid representation cannot occur
from decimal import Decimal, ROUND_HALF_UP

def prevented_discount(price, rate):
    # the type forbids binary float error by construction
    p = Decimal(str(price))
    r = Decimal(str(rate))
    return (p * r).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

print("prevented (Decimal):", prevented_discount(price, rate))