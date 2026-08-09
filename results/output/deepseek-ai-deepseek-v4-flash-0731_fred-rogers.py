def teach_recursion(n):
    # (1) Patience move: pause and look at the smallest case first.
    # We will not rush past the base case; it is the safe place to land.
    if n == 0:
        return 0
    # (2) Hard issue named calmly: recursion can feel like it never ends
    # when the stopping condition is missing. That is a property of the
    # code, not a flaw in the learner.
    return n + teach_recursion(n - 1)

def lesson():
    # (3) Concrete runnable demonstration: we show the call stack growing
    # and then unwinding, so the learner can see the path.
    steps = []
    def trace(n, depth=0):
        indent = "  " * depth
        steps.append(f"{indent}call teach_recursion({n})")
        if n == 0:
            steps.append(f"{indent}base case reached, return 0")
            return 0
        result = trace(n - 1, depth + 1)
        steps.append(f"{indent}return {n} + {result} = {n + result}")
        return n + result
    total = trace(3)
    steps.append(f"final result: {total}")
    return steps, total

steps, total = lesson()
# (4) Precise non-alarming instruction: "Add a base case that returns 0
# when n is 0. Do not call the function again after that return."
# This cannot be misread as "stop early" or "skip the work."
print("Lesson: recursion needs a base case that stops the calls.")
print("---")
for line in steps:
    print(line)
print("---")
# (5) Honest issue and actionable next step: the risk is infinite recursion
# if the base case is missing. Next step: test with n=0 and n=1, and check
# that the function returns without calling itself again.
assert teach_recursion(0) == 0
assert teach_recursion(1) == 1
assert teach_recursion(3) == 6
print("Next step: run the assertions above; they verify the base case works.")
print("Check: if n=0 returns 0 and n=1 returns 1, the stopping condition is sound.")