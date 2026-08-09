MAX_N = 100

def goldfish_sum(n):
    if not isinstance(n, int) or not 0 <= n <= MAX_N:
        raise ValueError("n must fit the packed 32-bit fields")
    state = n << 32
    while state >> 32:
        state = (((state >> 32) - 1) << 32) | ((state & 0xFFFFFFFF) + (state >> 32))
    return state & 0xFFFFFFFF

result = goldfish_sum(100)
plain = 100 * 101 // 2
assert result == plain
print({"result": result, "named_state_values": 1, "memory": "one register"})