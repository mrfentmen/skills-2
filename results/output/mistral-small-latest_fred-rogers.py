def count_up_to(n):
    """Count from 1 up to n, inclusive, using a for-loop."""
    result = []
    for i in range(1, n + 1):
        result.append(i)
    return result

# Let's take a quiet moment to look at one small idea: counting with a loop.
# The hard thing is that loops can sometimes run one step too far or not far enough.
# We'll show both the safe behavior and the unsafe behavior so we can see the difference.

# Safe behavior: counting up to 3 gives us [1, 2, 3]
assert count_up_to(3) == [1, 2, 3]

# Unsafe behavior: counting up to 0 gives us [] instead of [0] or causing an error
assert count_up_to(0) == []

# The honest issue is that counting from 1 to n requires careful handling of the range bounds.
# A precise instruction: use range(1, n + 1) to include n in the count.
# Your next step is to change the function so it counts from 0 up to n inclusive.

def count_up_to_zero_based(n):
    result = []
    for i in range(0, n + 1):
        result.append(i)
    return result

# Check that counting from 0 to 3 gives [0, 1, 2, 3]
assert count_up_to_zero_based(3) == [0, 1, 2, 3]

print({
    "demonstration": "complete",
    "safe_count": count_up_to(3),
    "zero_based_count": count_up_to_zero_based(3),
    "next_step": "try count_up_to_zero_based(5) and verify it returns [0, 1, 2, 3, 4, 5]"
})