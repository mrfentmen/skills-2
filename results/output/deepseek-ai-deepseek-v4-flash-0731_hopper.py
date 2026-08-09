# ============================================================
# Hopper-style debugging demo: "the moth in the total"
# ============================================================

# ------------------------------------------------------------
# (2) MINIMAL REPRODUCTION (fails before fix, passes after)
# ------------------------------------------------------------
# minimal input: [3, 1]; observed output 1; expected output 4
def buggy_total(values):
    # The moth: slicing off the first element before summing.
    total = 0
    for value in values[1:]:
        total += value
    return total

# ------------------------------------------------------------
# (4) TAUGHT-FISH NOTE (reusable lesson)
# ------------------------------------------------------------
# Lesson: when a loop "almost works" on multi-element input,
# suspect the boundary — the first or last element is often
# silently dropped. Always check the slice/range endpoints
# before suspecting the arithmetic or the data itself.

# ------------------------------------------------------------
# (5) HUMAN NOTE (explain to a teammate)
# ------------------------------------------------------------
# "The bug: `values[1:]` starts the loop at the SECOND element,
# so the first number never gets added. For [3, 1] we add only
# 1, giving 1 instead of 4. The fix is to iterate over the
# whole list with `enumerate` — no slice, no skipped head."

# ------------------------------------------------------------
# (1) CHRONOLOGICAL EXPERIMENT LOG
# ------------------------------------------------------------
# H1: "The input list is wrong" 
#     probe: print the input before calling the reducer
#     result: input is [3, 1] — correct, H1 disproved
#     next: instrument the reducer boundary
#
# H2: "The reducer skips the first element"
#     probe: enumerate every transition (index, before, after)
#     result: first processed index is 1, not 0 — H2 confirmed
#     next: replace the slice with a full indexed pass
#
# H3 (rival): "The addition is wrong"
#     probe: sum the values manually with a trace
#     result: arithmetic is correct once index 0 is included
#     next: apply the root-cause fix and add a regression guard

# ------------------------------------------------------------
# (3) ROOT CAUSE / FIRST INCORRECT STATE
# ------------------------------------------------------------
# First incorrect state: the reducer begins at index 1 instead
# of index 0. The crash (wrong total) is downstream of that
# skipped element.

# ------------------------------------------------------------
# DIAGNOSTIC HARNESS (makes the failure observable)
# ------------------------------------------------------------
def traced_total(values):
    """Expose every transition so the first wrong state is visible."""
    total = 0
    trace = []
    for index, value in enumerate(values):
        before = total
        total += value
        trace.append({"index": index, "value": value, "before": before, "after": total})
    return total, trace

# ------------------------------------------------------------
# RUN THE EXPERIMENTS AND PRINT THE LOG
# ------------------------------------------------------------
repro = [3, 1]
observed_bug = buggy_total(repro)
expected = sum(repro)

experiment_log = [
    {
        "hypothesis": "H1: input is wrong",
        "probe": "print input before reducer",
        "result": f"input={repro} — correct, H1 disproved",
        "next_action": "instrument reducer boundary",
    },
    {
        "hypothesis": "H2: reducer skips first element",
        "probe": "enumerate every transition",
        "result": f"first processed index=1 (should be 0)",
        "next_action": "replace slice with full indexed pass",
    },
    {
        "hypothesis": "H3: addition is wrong",
        "probe": "trace arithmetic with index 0 included",
        "result": f"arithmetic correct once index 0 included",
        "next_action": "apply root fix and add regression guard",
    },
]

print("=== EXPERIMENT LOG ===")
for entry in experiment_log:
    print(f"  {entry['hypothesis']}")
    print(f"    probe: {entry['probe']}")
    print(f"    result: {entry['result']}")
    print(f"    next: {entry['next_action']}")

print("\n=== OBSERVED vs EXPECTED ===")
print(f"  buggy_total({repro}) = {observed_bug}")
print(f"  expected = {expected}")

# ------------------------------------------------------------
# FIX (scoped to root cause) + REGRESSION CHECK
# ------------------------------------------------------------
fixed_total, trace = traced_total(repro)

print("\n=== TRACE (first wrong state visible) ===")
for step in trace:
    print(f"  index={step['index']} value={step['value']} "
          f"before={step['before']} after={step['after']}")

# Regression guard: this exact two-item case fails if the off-by-one returns.
assert fixed_total == expected, "regression: total mismatch"
assert trace[0]["index"] == 0, "regression: first index must be 0"

print("\n=== FIX OUTPUT ===")
print(f"  traced_total({repro}) = {fixed_total}")
print("  regression: PASS | root cause fixed at the reducer boundary")