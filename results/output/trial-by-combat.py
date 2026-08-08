import time
import random

# Shared contract
def contract(values):
    if not isinstance(values, list) or not all(isinstance(x, int) for x in values):
        raise TypeError("list[int] required")
    return sorted(values)

# Challenger 1: Merge sort
def merge_sort(values):
    if not isinstance(values, list) or not all(isinstance(x, int) for x in values):
        raise TypeError("list[int] required")
    arr = list(values)
    cost = 0
    def merge(left, right):
        nonlocal cost
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            cost += 1
            if left[i] <= right[j]:
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
        result.extend(left[i:]); result.extend(right[j:])
        return result
    def sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        return merge(sort(arr[:mid]), sort(arr[mid:]))
    return sort(arr), cost

# Challenger 2: Quick sort (Lomuto partition)
def quick_sort(values):
    if not isinstance(values, list) or not all(isinstance(x, int) for x in values):
        raise TypeError("list[int] required")
    arr = list(values)
    cost = 0
    def sort(lo, hi):
        nonlocal cost
        if lo >= hi:
            return
        pivot = arr[hi]
        i = lo
        for j in range(lo, hi):
            cost += 1
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[hi] = arr[hi], arr[i]
        sort(lo, i - 1)
        sort(i + 1, hi)
    sort(0, len(arr) - 1)
    return arr, cost

# Oracle
def oracle(values):
    return sorted(values)

# Challenge corpus
cases = [
    [],
    [1],
    [3, 1, 3, 2],
    [0, 0, 0],
    [-5, -1, -10],
    [5, 4, 3, 2, 1],
    [1, 2, 3, 4, 5],
    [random.randint(-100, 100) for _ in range(100)],
    [random.randint(-1000, 1000) for _ in range(1000)],
    "not-a-list",
    [1, "a", 3],
    [1.5, 2],
]

# Judge
def judge(fighter, cases):
    failures = []
    cost = 0
    for case in cases:
        expected_rejection = not isinstance(case, list) or not all(isinstance(x, int) for x in case)
        start = time.perf_counter()
        try:
            result, spent = fighter(case)
            elapsed = time.perf_counter() - start
            cost += spent + elapsed
            if expected_rejection:
                failures.append({"case": repr(case), "reason": "invalid input accepted"})
            elif result != oracle(case):
                failures.append({"case": case, "reason": "wrong result", "actual": result})
        except (TypeError, ValueError) as exc:
            if not expected_rejection:
                failures.append({"case": case, "reason": f"unexpected rejection: {exc}"})
        except Exception as exc:
            failures.append({"case": repr(case), "reason": f"unexpected: {exc}"})
    return {"failures": failures, "cost": cost, "valid": not failures}

# Run fight
scores = {
    "merge": judge(merge_sort, cases),
    "quick": judge(quick_sort, cases),
}

# Deterministic rule: valid first, then cost, then name
champion = min(
    (name for name, score in scores.items() if score["valid"]),
    key=lambda name: (scores[name]["cost"], name),
)

print({"champion": champion, "scores": scores})