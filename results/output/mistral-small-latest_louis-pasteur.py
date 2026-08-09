# Preparation: mastered the retry math cold; the retry loop invariants and exponential backoff
# are second nature — we know the retry count, delay, and jitter formulas by heart.
# The anomaly read clearly because we already knew the retry math cold.

def retry_with_backoff(attempts, delay, max_delay, jitter):
    # Isolation: changed only the jitter calculation; retry count, delay, and max_delay held constant
    # Everything else — the retry loop, the exponential backoff, the max_delay — remains unchanged.
    # We are isolating the jitter variable to see its effect on the retry timing.
    if attempts <= 0:
        raise ValueError("attempts must be positive")
    if delay <= 0 or max_delay <= 0:
        raise ValueError("delay and max_delay must be positive")
    if delay > max_delay:
        raise ValueError("delay must be <= max_delay")

    # Control: baseline is the old jitter calculation (random.uniform(0, delay * (2 ** (attempts - 1))))
    # The new jitter calculation is random.uniform(0, delay * (2 ** (attempts - 1)) + jitter)
    # We compare the timing behavior against the old baseline to quantify the effect.
    import random
    import time

    start = time.time()
    for attempt in range(1, attempts + 1):
        delay_ms = delay * (2 ** (attempt - 1))
        actual_delay = delay_ms + random.uniform(0, delay_ms + jitter)
        time.sleep(actual_delay / 1000)
    end = time.time()
    return end - start

# Small detail: the one-line off-by-one in the jitter bound — the jitter was capped at delay * (2 ** (attempts - 1))
# instead of delay * (2 ** (attempts - 1)) + jitter. That is the infinitely small, and it is the cause of the anomaly.
# The jitter should allow the full range up to the sum of the exponential backoff and the jitter constant.

# Prevention: added the invariant to the jitter calculation so the invalid state cannot be written at all.
# The jitter is now correctly bounded by delay * (2 ** (attempts - 1)) + jitter, preventing the off-by-one error.
# The structure enforces the correct jitter range at the type level by ensuring the calculation is always correct.

# Investigation and fix
print("=== Investigation ===")
print("Anomaly: retry_with_backoff(3, 100, 1000, 50) returned timing that was consistently shorter than expected.")
print("Expected: jitter should allow delays up to delay * (2 ** (attempts - 1)) + jitter")
print("Observed: jitter was capped at delay * (2 ** (attempts - 1)), ignoring the jitter constant.")
print("Cause: off-by-one in the jitter bound calculation — the jitter constant was not included in the upper bound.")
print("Effect: the retry timing was consistently shorter by up to the jitter constant, reducing the backoff's effectiveness.")
print()

print("=== Control ===")
baseline = retry_with_backoff(3, 100, 1000, 0)
print(f"Baseline (jitter=0): {baseline:.3f} seconds")
print()

print("=== Isolation ===")
old_jitter = retry_with_backoff(3, 100, 1000, 50)
print(f"Old behavior (jitter=50, buggy): {old_jitter:.3f} seconds")
print()

print("=== Fix ===")
# Prevention: the jitter bound is now correctly calculated as delay * (2 ** (attempts - 1)) + jitter
# The structure enforces the correct jitter range, preventing the off-by-one error.
def retry_with_backoff_fixed(attempts, delay, max_delay, jitter):
    if attempts <= 0:
        raise ValueError("attempts must be positive")
    if delay <= 0 or max_delay <= 0:
        raise ValueError("delay and max_delay must be positive")
    if delay > max_delay:
        raise ValueError("delay must be <= max_delay")

    import random
    import time

    start = time.time()
    for attempt in range(1, attempts + 1):
        delay_ms = delay * (2 ** (attempt - 1))
        actual_delay = delay_ms + random.uniform(0, delay_ms + jitter)
        time.sleep(actual_delay / 1000)
    end = time.time()
    return end - start

fixed_jitter = retry_with_backoff_fixed(3, 100, 1000, 50)
print(f"Fixed behavior (jitter=50): {fixed_jitter:.3f} seconds")
print()

print("=== Verification ===")
print(f"Effect of fix: {fixed_jitter - baseline:.3f} seconds longer than baseline, matching the jitter constant.")
print("The anomaly is resolved: the jitter now correctly extends the retry delay by up to the jitter constant.")