# Data model: a finite sequence of comparable items; empty input is valid.
# Idea: maintain a sorted prefix; insert the next item into its proper place.
# requires: values is a finite sequence of comparable items.
# ensures: output is sorted and contains exactly the input items (a permutation).
# invariant: before iteration i, output[:i] is sorted and is a permutation of values[:i].
# termination: each outer iteration increases the sorted prefix by one, so after len(values) iterations the whole sequence is sorted.
# complexity: O(n^2) worst case, O(1) auxiliary space beyond the copy; optimize only if profiling shows a real bottleneck.

def insertion_sort(values):
    """Return a sorted copy of values using the literate insertion-sort argument."""
    ordered = list(values)
    for i in range(1, len(ordered)):
        item = ordered[i]
        j = i - 1
        # invariant: ordered[:i] is sorted before insertion begins
        while j >= 0 and ordered[j] > item:
            ordered[j + 1] = ordered[j]
            j -= 1
        ordered[j + 1] = item
        assert ordered[: i + 1] == sorted(ordered[: i + 1])
    assert sorted(ordered) == sorted(values)  # postcondition: permutation preserved
    return ordered

# Example: [3, 1, 2] -> [1, 2, 3]. The assertion is the executable proof hook.
example = insertion_sort([3, 1, 2])
assert example == [1, 2, 3]
assert insertion_sort([]) == []       # edge case: empty data is valid
assert insertion_sort([7]) == [7]     # edge case: one item is already sorted
print(example)