def daisyworld(warm_pop, cold_pop, temp):
    # the loop: solar_flux -> albedo -> temp -> growth -> population -> albedo -> ...
    # opposing loops: warm daisies (absorb light, raise temp) vs cold daisies (reflect light, lower temp)
    # tipping-point watch: temp deviation from 22.5C; threshold is |ΔT| > 15C (growth collapses)
    # humility note: this model ignores clouds, oceans, and human activity — it is a toy, not a planet.
    growth = max(0.0, 1.0 - abs(temp - 22.5) / 15.0)  # daisies thrive near 22.5C
    warm_pop *= 1.0 + 0.05 * growth - 0.02 * (temp - 22.5)
    cold_pop *= 1.0 + 0.05 * growth + 0.02 * (temp - 22.5)
    new_temp = temp + 0.1 * (warm_pop - cold_pop)  # feedback loop, no planner
    return {"warm_pop": round(warm_pop, 2), "cold_pop": round(cold_pop, 2),
            "temp": round(new_temp, 2)}

state = {"warm_pop": 50.0, "cold_pop": 50.0, "temp": 20.0}
for _ in range(20):
    state = daisyworld(**state)
print(state)