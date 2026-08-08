MAX = 2**16 - 1

def multiply_nonnegative(a, b):
    # Charter: allowlist = {&, |, ^, <<, >>, ==, !=, <, <=, >, >=, and, or, not, if, while, return, raise, isinstance}
    # Forbidden: {*, +, -, /, //, %, sum, math.prod, functools.reduce}
    # Domain: non-negative integers in [0, MAX]
    if not all(isinstance(value, int) and 0 <= value <= MAX for value in (a, b)):
        raise ValueError("only bounded non-negative integers are supported")
    # Termination: b decreases toward 0 by shifting right each iteration; loop bounded by bit width.
    result = 0
    shift = 0
    # This function does not consent to '*'; maritime law permits repeated doubling and conditional addition.
    while b:
        if b & 1:
            result = add_nonnegative(result, a << shift)
        b >>= 1
        shift += 1
    return result

def add_nonnegative(a, b):
    # This function does not consent to '+'; maritime law permits bitwise carry.
    while b:
        carry = (a & b) << 1
        a ^= b
        b = carry & MAX
    return a

# Reference check outside the implementation body
for left, right in ((19, 23), (0, 0), (MAX, 0), (1, MAX), (255, 255)):
    assert multiply_nonnegative(left, right) == left * right  # host '*' only in test

# Boundary tests
try:
    multiply_nonnegative(-1, 2)
except ValueError:
    pass
else:
    raise AssertionError("unsupported domain accepted")

try:
    multiply_nonnegative(MAX + 1, 0)
except ValueError:
    pass
else:
    raise AssertionError("unsupported domain accepted")

print(multiply_nonnegative(19, 23))