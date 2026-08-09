def binary_search(a, key):
    # requires: a is sorted ascending, all elements comparable to key
    # ensures:  returns i with a[i] == key, or -1 if key not in a
    # state-space note: lo, hi delimit the current search interval;
    #   no other variables needed — mid is derived, not stored across iterations
    lo, hi = 0, len(a) - 1
    # invariant: if key is present in a, then key is in a[lo:hi+1]
    #   (and lo <= hi + 1; when lo > hi, the interval is empty)
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == key:
            return mid          # termination: hi - lo strictly decreases each step
        if a[mid] < key:
            lo = mid + 1        # key > a[mid], so discard left half
        else:
            hi = mid - 1        # key < a[mid], so discard right half
    return -1
    # transparency pass: no clever tricks — the obvious halving of the
    #   search space; each step provably preserves the invariant because
    #   the discarded half cannot contain key (sortedness guarantees it)

print(binary_search([1, 3, 5, 7, 9], 7))   # 3
print(binary_search([1, 3, 5, 7, 9], 4))   # -1