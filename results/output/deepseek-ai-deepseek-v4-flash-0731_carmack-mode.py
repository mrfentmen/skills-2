import time
import tracemalloc

def hot(data):
    return [x * 2 for x in data]

data = list(range(1_000_000))

# MEASURE FIRST — allocations and time before any optimization
tracemalloc.start()
t0 = time.perf_counter()
result = hot(data)
t1 = time.perf_counter()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

before_ms = (t1 - t0) * 1000
before_peak_kb = peak / 1024

# Only optimize if measurement justifies it — here we see the list comp allocates
# a full new list. The focused fix: preallocate and fill in place to cut allocation.
if before_ms > 0:
    def hot_optimized(data):
        out = [0] * len(data)
        for i, x in enumerate(data):
            out[i] = x << 1
        return out

    tracemalloc.start()
    t0 = time.perf_counter()
    result_opt = hot_optimized(data)
    t1 = time.perf_counter()
    current_opt, peak_opt = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    after_ms = (t1 - t0) * 1000
    after_peak_kb = peak_opt / 1024

    # correctness preserved
    assert result == result_opt

    print(f"before: {before_ms:.2f}ms, peak {before_peak_kb:.1f}KB")
    print(f"after:  {after_ms:.2f}ms, peak {after_peak_kb:.1f}KB")
    print(f"speedup: {before_ms / after_ms:.2f}x, allocation cut: {before_peak_kb - after_peak_kb:.1f}KB")