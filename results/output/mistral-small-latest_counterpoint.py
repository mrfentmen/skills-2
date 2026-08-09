import math
from collections import deque

def prime_factorization_voice(n):
    if n < 2:
        yield {"voice": "prime_factorization", "step": "base_case"}
        return []
    factors = []
    divisor = 2
    while n > 1:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
            yield {"voice": "prime_factorization", "step": f"divisor={divisor}, remaining={n}"}
        divisor += 1
    return factors

def binary_heap_sort_voice(arr):
    heap = []
    for item in arr:
        heap.append(item)
        yield {"voice": "binary_heap_sort", "step": f"inserted={item}, heap_size={len(heap)}"}
        i = len(heap) - 1
        while i > 0:
            parent = (i - 1) // 2
            if heap[i] >= heap[parent]:
                break
            heap[i], heap[parent] = heap[parent], heap[i]
            i = parent
            yield {"voice": "binary_heap_sort", "step": f"heapified_up, index={i}"}
    sorted_arr = []
    while heap:
        sorted_arr.append(heap[0])
        last = heap.pop()
        if heap:
            heap[0] = last
            i = 0
            while True:
                left = 2 * i + 1
                right = 2 * i + 2
                smallest = i
                if left < len(heap) and heap[left] < heap[smallest]:
                    smallest = left
                if right < len(heap) and heap[right] < heap[smallest]:
                    smallest = right
                if smallest == i:
                    break
                heap[i], heap[smallest] = heap[smallest], heap[i]
                i = smallest
                yield {"voice": "binary_heap_sort", "step": f"heapified_down, index={i}"}
    return sorted_arr

def counterpoint(n, arr):
    voices = [prime_factorization_voice(n), binary_heap_sort_voice(arr)]
    answers = [None, None]
    trace = []
    done = [False, False]
    while not all(done):
        for idx, voice in enumerate(voices):
            if done[idx]:
                continue
            try:
                step = next(voice)
                trace.append(step)
            except StopIteration as finished:
                answers[idx] = finished.value
                done[idx] = True
    report = {
        "answers": answers,
        "trace": trace,
        "status": "converged" if answers[0] == answers[1] else "diverged"
    }
    return report

report = counterpoint(123456789, [5, 3, 8, 1, 2])
print({
    "status": report["status"],
    "steps": len(report["trace"]),
    "first_voice_answer": report["answers"][0],
    "second_voice_answer": report["answers"][1]
})