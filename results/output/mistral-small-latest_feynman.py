# Recreate a tiny bubble sort from first principles
def recreate_bubble_sort(arr):
    n = len(arr)
    # primitive: swap adjacent if out of order, repeat until no swaps
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

# Trace the first three steps on [3, 1, 4, 1, 5]
trace_arr = [3, 1, 4, 1, 5]
print("trace step 0:", trace_arr)
recreate_bubble_sort(trace_arr)
print("trace step 1:", trace_arr)
trace_arr = [3, 1, 4, 1, 5]
recreate_bubble_sort(trace_arr)
print("trace step 2:", trace_arr)

# Ice-water: saturated memory / zero bandwidth — empty and single-element
print("extreme empty:", recreate_bubble_sort([]))
print("extreme single:", recreate_bubble_sort([42]))

# Falsification: the "guarantee" that bubble sort always returns a permutation of the input
original = [2, 1, 3]
sorted_out = recreate_bubble_sort(original.copy())
# try to break the permutation guarantee by mutating the output
sorted_out.append(99)
print("falsification attempt:", sorted_out, "vs original", original)