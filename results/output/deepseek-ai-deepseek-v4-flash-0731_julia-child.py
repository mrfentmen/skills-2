import time
import threading
from dataclasses import dataclass
from typing import List, Optional

# (1) MISE EN PLACE: environment, inputs, and tests prepared before the main work
# - Environment: Python 3.8+, standard library only (no external deps to fail)
# - Inputs: recipe steps as (name, seconds) tuples; hostile inputs: empty list,
#   negative/zero durations, non-numeric values, None
# - Tests: a self-check function that runs happy, empty, malformed, boundary cases
#   BEFORE the timer logic is trusted. Rollback: if any test fails, we print the
#   failure and refuse to start the timer — no half-cooked souffle.

@dataclass
class RecipeStep:
    name: str
    seconds: int

def _validate_steps(steps: List[RecipeStep]) -> Optional[str]:
    # the base validation: every step must have a name and a positive integer time
    if not isinstance(steps, list):
        return "steps must be a list"
    if len(steps) == 0:
        return "at least one step required"
    for i, step in enumerate(steps):
        if not isinstance(step, RecipeStep):
            return f"step {i} is not a RecipeStep"
        if not step.name or not isinstance(step.name, str):
            return f"step {i} has an invalid name"
        if not isinstance(step.seconds, int) or step.seconds <= 0:
            return f"step {i} has non-positive or non-integer seconds"
    return None

# (2) FUNDAMENTALS: the foundational technique here is a countdown loop with
#     a blocking sleep — the simplest reliable primitive. We master that before
#     adding any fancy threading or async. The loop is the base; everything else
#     is garnish.

def _countdown(seconds: int, step_name: str) -> None:
    # the fundamental: tick every second, print progress, no cleverness
    for remaining in range(seconds, 0, -1):
        print(f"  [{step_name}] {remaining}s left...", flush=True)
        time.sleep(1)

def run_recipe(steps: List[RecipeStep]) -> None:
    # the main work, but only after mise en place passes
    error = _validate_steps(steps)
    if error:
        raise ValueError(f"mise en place failed: {error}")

    print("Bon appétit! Starting the recipe timer.")
    for idx, step in enumerate(steps, start=1):
        print(f"\nStep {idx}: {step.name} ({step.seconds}s)")
        _countdown(step.seconds, step.name)
    print("\nDinner is served! The timer sang its last note.")

# (3) TEST LOOP: the work tested and re-tested until it executes reliably.
#     We run the validation against happy, empty, malformed, boundary, and
#     hostile inputs. The timer itself is tested with a 1-second step to keep
#     the loop fast. We iterate until all pass — no skipping the tasting.

def _test_validation() -> List[str]:
    failures = []
    # happy path
    happy = [RecipeStep("chop onions", 2), RecipeStep("sauté", 3)]
    if _validate_steps(happy) is not None:
        failures.append("happy path failed")

    # empty list
    if _validate_steps([]) is None:
        failures.append("empty list should fail")

    # malformed: not a list
    if _validate_steps("not a list") is None:
        failures.append("non-list should fail")

    # boundary: zero seconds
    if _validate_steps([RecipeStep("zero", 0)]) is None:
        failures.append("zero seconds should fail")

    # hostile: negative seconds
    if _validate_steps([RecipeStep("negative", -5)]) is None:
        failures.append("negative seconds should fail")

    # hostile: non-integer seconds
    if _validate_steps([RecipeStep("float", 2.5)]) is None:
        failures.append("float seconds should fail")

    # hostile: None step
    if _validate_steps([None]) is None:
        failures.append("None step should fail")

    return failures

def _test_timer() -> List[str]:
    failures = []
    # run a 1-second recipe to verify the countdown executes without exception
    try:
        run_recipe([RecipeStep("blink", 1)])
    except Exception as e:
        failures.append(f"timer execution failed: {e}")
    return failures

def run_tests() -> None:
    print("=== TEST LOOP: tasting the recipe before serving ===")
    failures = _test_validation() + _test_timer()
    if failures:
        print("The souffle fell! Failures:")
        for f in failures:
            print(f"  - {f}")
        raise SystemExit(1)
    print("All tests passed — the recipe is reliable enough for a home cook.")

# (4) FEARNESSLESSNESS NOTE: the fear is that a timer with hostile inputs will
#     crash mid-recipe and ruin dinner. The what-the-hell move: we validate
#     everything up front, but we still start — we don't let the fear of a
#     burned roux stop us from lighting the stove. We test, then we cook.

# (5) JOY CHECK: are we still interested? Yes — a timer that counts down with
#     a name for each step feels like a kitchen companion, not a chore. The
#     enthusiasm keeps the code honest and the output warm.

if __name__ == "__main__":
    # mise en place: tests first, then the real recipe
    run_tests()

    # the actual recipe — a tiny dinner timer
    my_recipe = [
        RecipeStep("melt butter", 2),
        RecipeStep("add flour and stir", 3),
        RecipeStep("whisk in stock", 4),
        RecipeStep("simmer until thick", 5),
    ]

    print("\n=== THE REAL RECIPE: a tiny sauce timer ===")
    run_recipe(my_recipe)