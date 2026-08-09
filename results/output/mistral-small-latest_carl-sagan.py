# claim: the function sorts any list of integers correctly. falsifiable: yes — any unsorted input produces a different output
# evidence bar: independent confirmation via a second sorting algorithm, same result
# baloney check: occam — the simplest explanation is a correct sort; multiple hypotheses — test bubble sort and quicksort
# balance note: open to new sorting methods, but they must beat the baseline on the same input
# plain explanation: imagine a line of people getting taller — the sort arranges them in order like a patient librarian shelving books

def baloney_kit(claim, tests, simplest_explains):
    return {
        "claim": claim,
        "falsifiable": any(t["can_fail"] for t in tests),
        "independently_confirmed": all(t["passed"] for t in tests),
        "occam_wins": simplest_explains,
        "accepted": (any(t["can_fail"] for t in tests)
                     and all(t["passed"] for t in tests)
                     and simplest_explains),
    }

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

test_input = [3, 1, 4, 1, 5, 9, 2, 6]
expected = [1, 1, 2, 3, 4, 5, 6, 9]

tests = [
    {"name": "bubble sort matches expected", "passed": bubble_sort(test_input.copy()) == expected, "can_fail": True},
    {"name": "quicksort matches expected", "passed": quicksort(test_input.copy()) == expected, "can_fail": True},
]

print(baloney_kit("the function sorts any list of integers correctly", tests, simplest_explains=True))