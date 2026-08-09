# unknown: the missing digit in the multiplication puzzle
# data: the multiplication layout
# condition: the product must be correct when the digit is restored
# plan: this resembles the classic cryptarithmetic puzzle; strategy = constraint propagation on digit positions
# related problem: the SEND+MORE=MONEY puzzle we solved last week

def solve_missing_digit():
    # carry-out: step-by-step digit assignment and constraint checking
    # We have:   3 9 ?
    #          ×    7
    #          -------
    #          2 7 ? 3
    # The ones digit of the product must be 3, so ? × 7 ≡ 3 (mod 10)
    # The only digit satisfying this is 9, because 9 × 7 = 63 → ones digit 3
    # Verify: 399 × 7 = 2793, which matches the given layout
    return 9

# look back: the solution holds for the given layout; a second derivation via multiplication rules also agrees
# easier problem: solve with a single-digit multiplier first, then scale the plan
print(solve_missing_digit())