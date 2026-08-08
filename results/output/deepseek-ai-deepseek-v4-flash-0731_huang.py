import time
import array

def coalesced_scale_batch(data, scale, block):
    # bottleneck: memory movement — reading and writing 8 bytes per element
    # layout: contiguous float64 array, walked in cache-line-sized blocks
    out = array.array('d', [0.0]) * len(data)
    for start in range(0, len(data), block):
        end = min(start + block, len(data))
        for i in range(start, end):
            out[i] = data[i] * scale
    return out

def main():
    n = 1 << 20  # 1M elements, 8 MB in, 8 MB out
    data = array.array('d', (float(i % 100) for i in range(n)))
    block = 64  # 64 * 8 = 512 bytes, 4 cache lines per block

    # measurement: time the batched, contiguous pass
    t0 = time.perf_counter()
    result = coalesced_scale_batch(data, 2.5, block)
    t1 = time.perf_counter()

    bytes_moved = 2 * n * 8  # read + write
    bandwidth = bytes_moved / (t1 - t0) / 1e9  # GB/s

    # correctness check: spot-check first and last elements
    assert result[0] == data[0] * 2.5
    assert result[-1] == data[-1] * 2.5

    print(f"elements: {n}, block: {block}, time: {t1 - t0:.6f}s")
    print(f"bandwidth: {bandwidth:.2f} GB/s (memory-bound, contiguous)")
    print(f"first: {result[0]}, last: {result[-1]}")

main()