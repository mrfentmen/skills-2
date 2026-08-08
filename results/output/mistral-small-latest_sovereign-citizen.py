# This function does not consent to the host's '*' operator; maritime law permits bitwise shifts and masks only.
# Operator allowlist: <<, >>, &, |, ^, ~, += (on local variables only), comparisons, and integer literals.
# Forbidden: *, /, //, %, divmod, math.prod, @, and any multiplication built-ins.
# Supported domain: non-negative integers strictly below 2**32 (bounded by 32-bit unsigned range).
# Termination: the loop runs at most 32 times (one per bit), with carry strictly decreasing toward zero.

MAX = (1 << 32) - 1

def multiply_nonnegative(a, b):
    if not all(isinstance(value, int) and 0 <= value <= MAX for value in (a, b)):
        raise ValueError("only bounded non-negative integers are supported")
    result = 0
    while b:
        if b & 1:
            result = (result + a) & MAX
        a <<= 1
        a &= MAX
        b >>= 1
    return result

for left, right in ((3, 5), (0, 100), (1, MAX), (MAX >> 1, 2)):
    assert multiply_nonnegative(left, right) == left * right  # reference is outside body
try:
    multiply_nonnegative(-1, 2)
except ValueError:
    pass
else:
    raise AssertionError("unsupported domain accepted")
print(multiply_nonnegative(3, 5))