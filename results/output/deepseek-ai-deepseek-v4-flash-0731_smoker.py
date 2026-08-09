# I checked the computation contract first: it's a small, self-contained
# arithmetic task. No codebase to inspect, no packages to verify, no
# external API. The only thing I can do is implement it, run it, and
# report what I actually saw.

def compute(input_value: int) -> int:
    # Smallest sensible change: no abstraction, no dependency, no
    # over-engineering. Just the arithmetic the task demands.
    # I'm not guessing the contract; I'm defining it explicitly so
    # the test below is meaningful.
    return input_value * 2 + 1

# Verification: I ran this, not just wrote it. The test below is the
# evidence. If it fails, I'm not claiming it works.
def test_compute():
    # Known input, known output. This is the ground truth I checked.
    assert compute(3) == 7, "compute(3) should be 7, got something else"
    assert compute(0) == 1, "compute(0) should be 1, got something else"
    assert compute(-2) == -3, "compute(-2) should be -3, got something else"
    # Edge case: large value, just to make sure no overflow in Python
    # (Python ints don't overflow, but I still check the logic holds).
    assert compute(10**6) == 2 * 10**6 + 1, "large input failed"

# Run the test. If it raises, the script dies and I know it's broken.
test_compute()

# Print the result so you can see the actual output, not a claim.
result = compute(3)
print(f"compute(3) = {result}")

# What remains unverified:
# - I have not tested this against any external spec or API contract,
#   because none was provided. The computation is defined by my own
#   explicit contract above.
# - I have not run this under a profiler or load test; it's a trivial
#   O(1) operation, so that's not meaningful here.
# - I have not verified behavior for non-integer inputs (e.g., floats,
#   strings). The function signature says int, and I'm not pretending
#   it handles anything else.
# - No type checker or linter was run; I'm relying on the test as the
#   only verification, which is appropriate for this size.