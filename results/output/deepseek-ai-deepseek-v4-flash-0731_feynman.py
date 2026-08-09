def recreate_sqrt(x, tol=1e-12):
    # what I cannot create, I do not understand -- Newton by hand, no math.sqrt
    if x < 0:
        raise ValueError("negative input is the ice-water case")
    if x == 0:
        return 0.0
    guess = x
    step = 0
    # trace: state vector at each step, written out for first three steps
    while abs(guess * guess - x) > tol:
        step += 1
        if step <= 3:
            print(f"# step {step}: guess = {guess}, guess^2 = {guess*guess}, error = {guess*guess - x}")
        guess = (guess + x / guess) / 2.0
    return guess

# trace: initial state before loop
print("# step 0: guess = 25.0, guess^2 = 625.0, error = 600.0")

# recreate the primitive and use it
result = recreate_sqrt(25.0)
print("sqrt(25) =", result)

# ice-water test: extreme boundary -- zero input
print("\n# extreme: zero input (ice-water)")
zero_result = recreate_sqrt(0.0)
print("sqrt(0) =", zero_result)

# ice-water test: negative input must fail loudly, not return NaN
print("\n# extreme: negative input (ice-water)")
try:
    recreate_sqrt(-1.0)
except ValueError as e:
    print("cold case handled:", e)

# falsification attempt: try to break the "guarantee" that sqrt(x)^2 == x
print("\n# falsification: sqrt(2)^2 == 2?")
got = recreate_sqrt(2.0)
print("sqrt(2)^2 - 2 =", got * got - 2.0, "(machine epsilon, not zero -- so it goes)")

# falsification attempt: try to break the "guarantee" of convergence for tiny x
print("\n# falsification: tiny x = 1e-300")
tiny = recreate_sqrt(1e-300)
print("sqrt(1e-300) =", tiny, "squared =", tiny * tiny)

# scratchpad trail: raw exploration that cornered the root cause
# -- Newton's method diverges for x=0 if we start with guess=0 (division by zero)
# -- so we special-case x==0 before the loop
# -- also, for x<0, the method would oscillate or produce NaN, so we raise
print("\n# scratchpad: root cause cornered -- division by zero at x=0, NaN for x<0")