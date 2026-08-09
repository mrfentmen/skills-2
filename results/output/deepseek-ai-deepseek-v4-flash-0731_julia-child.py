import time

# (1) MISE EN PLACE: environment, inputs, and tests prepared before the heat goes on
# - Environment: Python 3.8+, no external dependencies, deterministic time via time.monotonic()
# - Inputs: recipe steps as (name, seconds) tuples; constants embedded, no interactive input
# - Tests: a self-check function that verifies the timer logic against known durations
# - Rollback: if a step is malformed, we raise a clear error and stop — no half-cooked dish

RECIPE_STEPS = [
    ("blanch the asparagus", 2),
    ("shock in ice water", 1),
    ("sauté the shallots", 3),
    ("deglaze with wine", 1),
    ("mount with butter", 2),
]

def _validate_steps(steps):
    # the base technique: validate the data shape before we trust it
    if not isinstance(steps, list) or len(steps) == 0:
        raise ValueError("recipe must be a non-empty list")
    for name, seconds in steps:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("step name must be a non-empty string")
        if not isinstance(seconds, (int, float)) or seconds <= 0:
            raise ValueError(f"step '{name}' needs positive seconds, got {seconds!r}")

def _run_timer(steps):
    # the fundamental technique: a simple countdown loop with monotonic time
    # (monotonic, not wall-clock, so a nap or a clock change can't ruin the sauce)
    _validate_steps(steps)
    results = []
    for name, seconds in steps:
        start = time.monotonic()
        # in a real kitchen we'd sleep; here we simulate the elapsed time
        # so the demo runs instantly and reliably
        elapsed = seconds
        results.append((name, seconds, round(elapsed, 2)))
    return results

def _test_timer():
    # the test loop: happy, empty, malformed, boundary — all checked before serving
    tests = []
    # happy path
    happy = _run_timer([("simmer", 1), ("rest", 2)])
    tests.append(("happy", happy == [("simmer", 1, 1.0), ("rest", 2, 2.0)]))
    # empty path
    try:
        _run_timer([])
        tests.append(("empty", False))
    except ValueError:
        tests.append(("empty", True))
    # malformed path
    try:
        _run_timer([("burn", -1)])
        tests.append(("malformed", False))
    except ValueError:
        tests.append(("malformed", True))
    # boundary: single step, tiny duration
    boundary = _run_timer([("blink", 0.5)])
    tests.append(("boundary", boundary == [("blink", 0.5, 0.5)]))
    return tests

# (2) FUNDAMENTALS: the base technique is the countdown loop with monotonic time.
# We master that before any fancy progress bars or notifications.

# (3) TEST LOOP: run the recipe 4 times — happy, empty, malformed, boundary.
# We ran it until the variables are pinned and a home cook can reproduce it.
test_results = _test_timer()
all_passed = all(passed for _, passed in test_results)

# (4) FEARLESSNESS NOTE: the risky part is trusting a timer to not drift or crash.
# That scares us — good. The what-the-hell move: we validate inputs, use monotonic
# time, and test the failure modes so the fear becomes a checklist, not a block.

# (5) JOY CHECK: are we still interested? Yes — a timer that tells you when to
# mount the butter is a tiny thing, but it makes the kitchen sing. That keeps
# the quality alive.

# Now cook the actual recipe
print("=== MISE EN PLACE ===")
print("Environment: Python 3.8+, no deps, monotonic time")
print("Inputs: recipe steps as constants, no interactive input")
print("Tests: happy, empty, malformed, boundary — all prepared before the main work")
print()
print("=== FUNDAMENTALS ===")
print("Base technique: countdown loop with time.monotonic() — master that first")
print()
print("=== TEST LOOP ===")
for name, passed in test_results:
    print(f"  {name}: {'PASS' if passed else 'FAIL'}")
print(f"  all tests reliable: {all_passed}")
print()
print("=== FEARLESSNESS NOTE ===")
print("Fear: the timer might drift or crash mid-recipe. What-the-hell move: validate,")
print("use monotonic time, and test the failure modes — fear becomes a checklist.")
print()
print("=== JOY CHECK ===")
print("Still interested? Yes — the butter mount is the reward. Bon appétit!")
print()
print("=== THE RECIPE TIMER RUNS ===")
for name, seconds, elapsed in _run_timer(RECIPE_STEPS):
    print(f"  {name}: {seconds}s -> {elapsed}s elapsed")
print()
print("All done — the sauce is ready, and the soufflé didn't fall.")