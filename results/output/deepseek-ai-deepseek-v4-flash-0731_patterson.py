import time

def compute(items):
    # common case: uniform multiply-add over the whole list
    return [x * 2 + 1 for x in items]

def measure(fn, items, reps=3):
    t0 = time.perf_counter()
    for _ in range(reps):
        fn(items)
    t1 = time.perf_counter()
    return (t1 - t0) / reps

data = list(range(1_000_000))

# measurement pass: identify bottleneck
t_baseline = measure(compute, data)
print(f"baseline={t_baseline:.4f}s")

# Amdahl analysis: the change touches the entire loop body
touched = 0.95  # fraction of work in the multiply-add loop
ceiling = 1 / (1 - touched)
print(f"touched={touched:.2f} ceiling={ceiling:.2f}x")

# common-case optimization: replace list comprehension with in-place loop
def compute_fast(items):
    # common case: uniform in-place operation, no allocation
    for i in range(len(items)):
        items[i] = items[i] * 2 + 1
    return items

# re-measurement
t_optimized = measure(compute_fast, data)
print(f"optimized={t_optimized:.4f}s")
print(f"speedup={t_baseline / t_optimized:.2f}x")