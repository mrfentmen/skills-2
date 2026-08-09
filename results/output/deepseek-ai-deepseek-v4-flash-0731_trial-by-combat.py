import time
import random

# Shared contract:
# Input: list of ints (may be empty, may contain duplicates, may be malformed)
# Output: (sorted_list, cost) where cost is a comparable numeric metric
# Invalid input policy: raise TypeError for non-list or non-int elements

# Independent oracle: pure reference implementation
def oracle(values):
    return sorted(values)

# Challenger 1: Merge sort (recursive, stable, O(n log n))
def merge_sort_fighter(values):
    if not isinstance(values, list) or not all(isinstance(x, int) for x in values):
        raise TypeError("list[int] required")
    cost = 0
    def merge_sort(arr):
        nonlocal cost
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            cost += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    return merge_sort(list(values)), cost

# Challenger 2: Quick sort (in-place, average O(n log n), worst O(n^2))
def quick_sort_fighter(values):
    if not isinstance(values, list) or not all(isinstance(x, int) for x in values):
        raise TypeError("list[int] required")
    cost = 0
    def quick_sort(arr, low, high):
        nonlocal cost
        if low < high:
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                cost += 1
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            pi = i + 1
            quick_sort(arr, low, pi - 1)
            quick_sort(arr, pi + 1, high)
    arr = list(values)
    quick_sort(arr, 0, len(arr) - 1)
    return arr, cost

# Fixed challenge corpus: normal, edge, duplicate, boundary, malformed, adversarial
cases = [
    [],                                    # empty
    [1],                                   # single
    [3, 1, 3, 2],                          # duplicates
    [0, -1, 2, -3, 4],                     # mixed signs
    [5, 4, 3, 2, 1],                       # reverse sorted
    [1, 2, 3, 4, 5],                       # already sorted
    [2, 2, 2, 2],                          # all same
    [-10**6, 10**6, 0, -1, 1],             # large values
    [random.randint(-100, 100) for _ in range(100)],  # random normal
    "not-a-list",                          # malformed: string
    [1, "two", 3],                         # malformed: mixed types
    None,                                  # malformed: None
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],       # boundary length
    [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],       # boundary reverse
]

# Deterministic judge: correctness gate first, then cost, then name tie-break
def judge(fighter, cases):
    failures = []
    cost = 0
    for case in cases:
        expected_rejection = not isinstance(case, list) or not all(isinstance(x, int) for x in case)
        try:
            result, spent = fighter(case)
            cost += spent
            if expected_rejection:
                failures.append({"case": repr(case), "reason": "invalid input was accepted"})
            elif result != oracle(case):
                failures.append({"case": case, "reason": "wrong result", "actual": result})
        except (TypeError, ValueError) as exc:
            if not expected_rejection:
                failures.append({"case": case, "reason": f"unexpected rejection: {exc}"})
        except Exception as exc:
            failures.append({"case": repr(case), "reason": f"unexpected: {exc}"})
    return {"failures": failures, "cost": cost, "valid": not failures}

# Run both fighters independently
score_merge = judge(merge_sort_fighter, cases)
score_quick = judge(quick_sort_fighter, cases)

# Declared rule: valid fighters only, min cost, then name tie-break
scores = {"merge": score_merge, "quick": score_quick}
valid_fighters = [name for name, score in scores.items() if score["valid"]]
if not valid_fighters:
    champion = None
else:
    champion = min(valid_fighters, key=lambda name: (scores[name]["cost"], name))

# Assertions to enforce the rule
assert champion is not None, "No valid challenger"
assert scores[champion]["valid"], "Champion must be valid"
for name, score in scores.items():
    if name != champion:
        assert not score["valid"] or (score["cost"], name) >= (scores[champion]["cost"], champion), "Tie-break violated"

# Print full diagnostics for both winner and loser
print({"champion": champion, "scores": scores})