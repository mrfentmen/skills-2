# contract: return the product of every integer in the list, including an empty input -> 1

def product_reference(values):
    # Strategy A: explicit fold, the easy-to-audit reference.
    if not isinstance(values, list) or any(not isinstance(v, int) or isinstance(v, bool) for v in values):
        raise TypeError("contract requires a list of integers")
    total = 1
    for value in values:
        total *= value
    return total

def product_recursive(values):
    # Strategy B: recursive splitting; structurally independent from the fold.
    if not isinstance(values, list) or any(not isinstance(v, int) or isinstance(v, bool) for v in values):
        raise TypeError("contract requires a list of integers")
    if not values:
        return 1
    middle = len(values) // 2
    return (product_recursive(values[:middle])
            * product_recursive(values[middle:])) if middle else values[0]

def outcome(fn, case):
    try:
        return ("ok", fn(case))
    except (TypeError, ValueError) as error:
        return ("error", type(error).__name__)

def reduce_counterexample(case, mismatch):
    # Try smaller halves until no smaller failing list remains.
    if not isinstance(case, list):
        return case
    candidate = case
    changed = True
    while changed and len(candidate) > 1:
        changed = False
        for smaller in (candidate[:len(candidate) // 2], candidate[1:]):
            if smaller and mismatch(smaller):
                candidate, changed = smaller, True
                break
    return candidate

def compare(cases):
    for case in cases:
        reference = outcome(product_reference, case)
        challenger = outcome(product_recursive, case)
        if reference != challenger:
            mismatch = lambda smaller: outcome(product_reference, smaller) != outcome(product_recursive, smaller)
            minimal = reduce_counterexample(case, mismatch)
            raise AssertionError(
                f"counterexample: input={case!r}, minimal={minimal!r}, "
                f"reference={reference}, challenger={challenger}"
            )
    return {"cases_compared": len(cases), "status": "agree; evidence, not proof"}

cases = [[], [7], [1, -2, 3], list(range(1, 21)), [0, 0, 0],
         [10**100, -10**100], None, ["malformed"], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
print(compare(cases))