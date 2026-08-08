import time
import tracemalloc
import array

def compute_sum(data):
    total = 0
    for x in data:
        total += x
    return total

# Baseline measurement
data = list(range(1_000_000))
tracemalloc.start()
t0 = time.perf_counter()
result = compute_sum(data)
t1 = time.perf_counter()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"Baseline: {len(data)} items")
print(f"  Time: {(t1 - t0) * 1000:.2f} ms")
print(f"  Peak memory: {peak / 1024 / 1024:.2f} MB")
print(f"  Result: {result}")

# Optimized measurement: use array.array for compact storage
tracemalloc.start()
t0 = time.perf_counter()
data_array = array.array('i', range(1_000_000))
result_array = compute_sum(data_array)
t1 = time.perf_counter()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"\nOptimized: array.array storage")
print(f"  Time: {(t1 - t0) * 1000:.2f} ms")
print(f"  Peak memory: {peak / 1024 / 1024:.2f} MB")
print(f"  Result: {result_array}")