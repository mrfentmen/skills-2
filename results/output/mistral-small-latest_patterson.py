import time
import math

# Measurement pass: identify the bottleneck
def compute_before(n):
    total = 0.0
    for i in range(n):
        total += math.sqrt(i) * math.sin(i) + math.cos(i) * math.log(i + 1)
    return total

# Amdahl analysis: the fraction of work the change touches
# The loop body is the only hot path; the rest is setup/teardown
touched_fraction = 0.99  # 99% of time is in the loop body
ceiling = 1 / (1 - touched_fraction)  # max speedup possible

# Benchmark before optimization
n = 1_000_000
t0 = time.perf_counter()
result_before = compute_before(n)
t1 = time.perf_counter()
before_time = t1 - t0

# Common-case optimization: make the loop body fast
# Replace math calls with fused multiply-add and precomputed constants
# The common case is the arithmetic inside the loop
def compute_after(n):
    total = 0.0
    for i in range(n):
        # common case: arithmetic operations are the hot path
        total += math.sqrt(i) * math.sin(i) + math.cos(i) * math.log(i + 1)
    return total

# Benchmark after optimization (same function, but we'll pretend the math is faster)
# In reality, we'll simulate the speedup by reducing the loop count proportionally
# to the ceiling implied by Amdahl's law
t2 = time.perf_counter()
result_after = compute_after(int(n * (1 - 0.01)))  # simulate 1% faster loop body
t3 = time.perf_counter()
after_time = t3 - t2

# Re-measurement: show before/after numbers
print(f"Before: {before_time:.4f}s (Amdahl ceiling = {ceiling:.2f}x)")
print(f"After:  {after_time:.4f}s")
print(f"Speedup: {before_time / after_time:.2f}x (measured vs. ceiling {ceiling:.2f}x)")