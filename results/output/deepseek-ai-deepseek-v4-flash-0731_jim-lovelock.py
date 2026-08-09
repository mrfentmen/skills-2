def daisyworld(warm_pop, cold_pop, temp, solar):
    # (1) whole-system view: the loop that keeps the system stable, end to end:
    # solar input -> absorbed by daisies (warm raises temp, cold lowers) ->
    # temperature -> daisy growth rates -> population mix -> albedo -> temp.
    # the loop closes: no external thermostat, only the daisies' own feedback.

    # (2) feedback model: opposing loops, not setpoints:
    #   warm daisies: higher temp -> lower growth (negative feedback on warming)
    #   cold daisies: higher temp -> higher growth (negative feedback on cooling)
    #   together they push temp toward the daisies' preferred band (~22C).

    # (3) daisyworld: the smallest model demonstrating regulation:
    #   two species, one warm one cold, competing via growth rates that
    #   depend on temperature; the mix adjusts to stabilize the planet.

    # (4) tipping-point watch: the threshold metric, not just the average:
    #   watch the *distance from the preferred temperature* (|temp - 22|).
    #   when that distance exceeds 15, growth collapses to zero — the system
    #   flips to a dead state. the average temp alone hides this cliff.

    # (5) humility note: this model does not claim to know real planetary
    #   albedo dynamics, ocean heat transport, or cloud feedbacks. it only
    #   demonstrates that opposing loops can regulate — not that they always do.

    growth = max(0.0, 1.0 - abs(temp - 22.0) / 15.0)  # daisies like ~22C
    warm_pop *= 1.0 + 0.05 * growth - 0.02 * (temp - 22.0)
    cold_pop *= 1.0 + 0.05 * growth + 0.02 * (temp - 22.0)
    new_temp = temp + 0.1 * (warm_pop - cold_pop) + 0.01 * (solar - 1.0)
    return {"warm_pop": round(warm_pop, 2), "cold_pop": round(cold_pop, 2),
            "temp": round(new_temp, 2), "solar": solar}

state = {"warm_pop": 50.0, "cold_pop": 50.0, "temp": 20.0, "solar": 1.0}
for step in range(20):
    state = daisyworld(**state)
    # tipping-point watch: print the threshold distance, not just temp
    threshold_distance = abs(state["temp"] - 22.0)
    print(f"step {step:2d}: temp={state['temp']:5.2f} warm={state['warm_pop']:5.2f} "
          f"cold={state['cold_pop']:5.2f} |temp-22|={threshold_distance:5.2f}")

# now perturb solar to show the regulation holds, then watch for the flip
print("\n--- solar shock: solar=1.5 ---")
state = {"warm_pop": 50.0, "cold_pop": 50.0, "temp": 20.0, "solar": 1.5}
for step in range(20):
    state = daisyworld(**state)
    threshold_distance = abs(state["temp"] - 22.0)
    print(f"step {step:2d}: temp={state['temp']:5.2f} warm={state['warm_pop']:5.2f} "
          f"cold={state['cold_pop']:5.2f} |temp-22|={threshold_distance:5.2f}")