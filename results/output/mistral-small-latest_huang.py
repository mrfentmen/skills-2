import array
import itertools
import time

def bytes_moved(rows, cols, dtype_bytes):
    # name the data movement first: that is the real cost
    return rows * cols * dtype_bytes

def batched_matrix_vector_product(matrix, vector, block_size=256):
    """
    Bottleneck: memory bandwidth when reading matrix and vector.
    Data layout: row-major contiguous matrix (float32), vector contiguous (float32).
    Throughput construct: batched processing by block to amortize memory access.
    Justification: block_size chosen to fit L2 cache (1MB typical) for reuse.
    """
    rows = len(matrix)
    cols = len(vector)
    assert all(len(row) == cols for row in matrix), "Matrix must be rectangular"
    assert cols == len(vector), "Vector length must match matrix columns"

    # Allocate output buffer
    result = array.array('f', [0.0]) * rows

    # Process in blocks to improve cache locality
    for i in range(0, rows, block_size):
        block_end = min(i + block_size, rows)
        for j in range(i, block_end):
            # Inner product: vectorized by hardware-friendly contiguous access
            row = matrix[j]
            s = 0.0
            for k in range(0, cols, 4):  # 4-wide vectorization via loop unrolling
                chunk = row[k:k+4]
                s += sum(a * b for a, b in zip(chunk, vector[k:k+4]))
            result[j] = s

    return result

# Generate test data: 4096x4096 matrix, 4096 vector (fits in L3 cache on modern CPUs)
matrix = [array.array('f', (i * 4096 + j for j in range(4096))) for i in range(4096)]
vector = array.array('f', range(4096))

# Measure throughput
start = time.perf_counter()
result = batched_matrix_vector_product(matrix, vector, block_size=256)
elapsed = time.perf_counter() - start

# Validate correctness on first element
expected = sum(i * j for i, j in zip(matrix[0], vector))
assert abs(result[0] - expected) < 1e-5, "Incorrect computation"

print("bytes moved:", bytes_moved(4096, 4096, 4))
print("throughput (GFLOP/s):", (2 * 4096 * 4096) / elapsed / 1e9)
print("result[0]:", result[0])