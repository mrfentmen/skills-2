def binary_search(haystack, needle):
    """Locate the index of `needle` in a sorted sequence `haystack`.

    Data model:
        haystack: a finite, non-empty sequence of comparable items in strictly
                  increasing order; duplicates are not allowed.
        needle:   an item comparable to the elements of `haystack`.
        indices:  integers in the range [0, len(haystack) - 1].

    Algorithm:
        Maintain two pointers, `lo` and `hi`, that delimit the *search window*
        within which `needle` must lie if it is present.  At each iteration,
        compare `needle` to the middle element of the window.  If equal, return
        the index.  If `needle` is smaller, discard the right half; otherwise
        discard the left half.  The window shrinks until it is empty or the
        element is found.

    Contract:
        requires: haystack is sorted and non-empty
        ensures:  returns the unique index i such that haystack[i] == needle,
                  or -1 if needle is not in haystack
        invariant: at the start of each iteration, needle ∈ haystack[lo..hi]
                   or needle ∉ haystack[0..hi] ∪ haystack[lo..n-1]
        termination: lo > hi guarantees the search window is empty; each
                     iteration reduces the window size by at least one, so
                     termination occurs after at most ⌈log₂ n⌉ iterations.

    Complexity:
        Time: O(log n) comparisons; O(1) auxiliary space.
        No premature optimization: the logarithmic bound is optimal for
        comparison-based search; any further speed-up would require a stronger
        data structure (e.g., hash table) whose overhead is unjustified for
        small or read-only sequences.
    """

    lo, hi = 0, len(haystack) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if haystack[mid] == needle:
            return mid
        if needle < haystack[mid]:
            hi = mid - 1
        else:
            lo = mid + 1
    return -1

# Example block (executable literature)
# input -> output
example = binary_search([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 23)
assert example == 5, f"Expected index 5, got {example}"

# Edge case: needle not present
assert binary_search([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 100) == -1

# Edge case: single-element sequence
assert binary_search([42], 42) == 0
assert binary_search([42], 0) == -1

# Postcondition check: every element is found at its correct position
for idx, val in enumerate([2, 5, 8, 12, 16, 23, 38, 56, 72, 91]):
    assert binary_search([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], val) == idx

print(example)