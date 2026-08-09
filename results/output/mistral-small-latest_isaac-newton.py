# standing on: Python's built-in sorted() — audited stdlib implementation, not hand-rolled
# conclusion: the list is sorted in non-decreasing order (deduced from the sorted() output).
# falsifier: any pair (a, b) with a > b in the output.
# the test that fails if wrong: assert output[i] <= output[i+1] for all i in range(len(output)-1)
# verified: the primitive alone, then the pipeline — each step green before the next
# not claimed: stability under concurrent mutation — we only verified the single-threaded path

def verify_sort_claim(input_list):
    # Step 1: isolate the primitive — Python's sorted() is the audited foundation
    output = sorted(input_list)

    # Step 2: verify the invariant on the output
    for i in range(len(output) - 1):
        if output[i] > output[i + 1]:
            raise AssertionError(f"Claim falsified at index {i}: {output[i]} > {output[i+1]}")

    # Step 3: return the demonstrated result
    return output

# Demonstration run
if __name__ == "__main__":
    test_input = [3, 1, 4, 1, 5, 9, 2, 6]
    result = verify_sort_claim(test_input)
    print("Proof walkthrough:")
    print(f"Input:  {test_input}")
    print(f"Output: {result}")
    print("Claim verified: the list is sorted in non-decreasing order.")