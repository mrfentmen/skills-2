def bubble_sort(values):
    if not isinstance(values, list) or not all(isinstance(x, (int, float)) for x in values):
        raise TypeError("list[number] required")
    work = list(values)
    comparisons = 0
    for end in range(len(work) - 1, 0, -1):
        for i in range(end):
            comparisons += 1
            if work[i] > work[i + 1]:
                work[i], work[i + 1] = work[i + 1], work[i]
    return work, comparisons

def merge_sort(values):
    if not isinstance(values, list) or not all(isinstance(x, (int, float)) for x in values):
        raise TypeError("list[number] required")
    def _merge_sort(arr):
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        left, left_cost = _merge_sort(arr[:mid])
        right, right_cost = _merge_sort(arr[mid:])
        merged = []
        i = j = 0
        comparisons = left_cost + right_cost
        while i < len(left) and j < len(right):
            comparisons += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, comparisons
    return _merge_sort(values)

def oracle(values):
    return sorted(values)

def judge(fighter, cases):
    failures, cost = [], 0
    for case in cases:
        expected_rejection = not isinstance(case, list) or not all(isinstance(x, (int, float)) for x in case)
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

cases = [
    [],
    [3, 1, 3, 2],
    [0],
    [-2, -2],
    [1.5, -1.5, 0.0],
    [9, 8, 7, 6, 5, 4, 3, 2, 1],
    [1],
    [10**6] * 10,
    "not-a-list",
    [None],
    [3, "2", 1],
    [float('inf'), float('-inf'), 0],
]
score_a = judge(bubble_sort, cases)
score_b = judge(merge_sort, cases)
scores = {"bubble": score_a, "merge": score_b}
champion = min(
    (name for name, score in scores.items() if score["valid"]),
    key=lambda name: (scores[name]["cost"], name),
)
print({"champion": champion, "scores": scores})