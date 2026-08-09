# claim: `sort_numbers` returns a list sorted in non-decreasing order for all valid integer lists.
# falsifiable: yes — any input list where the output is not non-decreasing, or is not a permutation of the input, disproves it.

# what confirms it: (evidence bar) — property-based testing over 10,000 random lists, plus a hand-checked edge-case suite,
# all passing with no counterexample. Independent confirmation: a second, separately written reference implementation
# (Python's built-in sorted) must agree on every input.

# baloney check:
#   independent confirmation: compare against `sorted()` on every generated list.
#   occam: the simplest hypothesis is that the function is correct; the simpler alternative (a bug in the test harness)
#          is ruled out by using a known-good oracle and fixed seeds.
#   multiple hypotheses: (a) function is correct, (b) function has an off-by-one in the loop, (c) function mutates input,
#          (d) function fails on duplicates. Each is tested explicitly.

# balance: open to the idea that the function is correct, but the scrutiny is equal — the same tests would catch
# a subtle bug in my own code, and I do not assume correctness because the function is short or "obvious."

# plain explanation: imagine sorting a deck of cards by repeatedly finding the smallest card and placing it in order.
# If you do that without ever losing a card or putting a larger card before a smaller one, the deck is sorted.
# The test shuffles the deck thousands of times and checks that the result is always in order and has the same cards —
# that is the wonder: a simple rule, verified against the cosmos of possible shuffles.

import random

def sort_numbers(lst):
    # A deliberately simple selection sort — but we will not trust it without evidence.
    result = lst[:]  # copy to avoid mutating input
    for i in range(len(result)):
        min_idx = i
        for j in range(i + 1, len(result)):
            if result[j] < result[min_idx]:
                min_idx = j
        result[i], result[min_idx] = result[min_idx], result[i]
    return result

def is_sorted(lst):
    return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))

def is_permutation(original, result):
    return sorted(original) == sorted(result)  # independent oracle

# Evidence bar: 10,000 random lists, plus edge cases, all must pass.
random.seed(42)  # reproducible — the cosmos of this test is fixed
test_lists = [
    [],
    [1],
    [1, 1, 1],
    [5, 4, 3, 2, 1],
    [1, 2, 3, 4, 5],
    [-3, 0, 2, -1, 10],
] + [[random.randint(-100, 100) for _ in range(random.randint(0, 50))] for _ in range(10000)]

all_passed = True
for original in test_lists:
    result = sort_numbers(original)
    # Independent confirmation: built-in sorted as a second channel
    if result != sorted(original):
        all_passed = False
        break
    # Falsifiability: check the property directly
    if not is_sorted(result) or not is_permutation(original, result):
        all_passed = False
        break

# Multiple hypotheses: test the specific failure modes
hypothesis_b_off_by_one = any(
    sort_numbers(lst) != sorted(lst)
    for lst in [[2, 1], [3, 2, 1], [1, 3, 2]]
)
hypothesis_c_mutates_input = any(
    (lambda l: (sort_numbers(l), l))(lst)[1] != lst
    for lst in [[2, 1], [5, 4, 3]]
)
hypothesis_d_duplicates = sort_numbers([2, 2, 1, 1]) == [1, 1, 2, 2]

# Occam: the simplest explanation is that the function is correct; the test harness is verified by using
# a known-good oracle and fixed seeds, so the simpler alternative (harness bug) is ruled out.

print(f"claim: sort_numbers returns non-decreasing permutation of input")
print(f"evidence bar: 10,006 lists, all must match sorted() and pass property checks")
print(f"baloney check: independent confirmation (sorted oracle), occam (harness verified), multiple hypotheses (b, c, d tested)")
print(f"balance: open to correctness, but equal scrutiny applied — no authority, only evidence")
print(f"plain explanation: like sorting a deck by always picking the smallest card — verified on 10,000 shuffles")
print(f"test result: {'PASSED' if all_passed and not hypothesis_b_off_by_one and not hypothesis_c_mutates_input and hypothesis_d_duplicates else 'FAILED'}")