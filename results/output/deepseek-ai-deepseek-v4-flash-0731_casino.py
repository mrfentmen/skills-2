import math
import random

def estimate_pi(trials, seed):
    if not isinstance(trials, int) or trials <= 0:
        raise ValueError("trials must be a positive integer")
    rng = random.Random(seed)
    hits = sum(rng.random() ** 2 + rng.random() ** 2 <= 1 for _ in range(trials))
    proportion = hits / trials
    z = 1.96
    denominator = 1 + z * z / trials
    centre = (proportion + z * z / (2 * trials)) / denominator
    radius = z * math.sqrt((proportion * (1 - proportion) + z * z / (4 * trials)) / trials) / denominator
    return {"trials": trials, "estimate": 4 * proportion, "low": 4 * (centre - radius), "high": 4 * (centre + radius), "hits": hits}

reports = [estimate_pi(trials, seed=7) for trials in (1_000, 10_000, 100_000)]
assert reports[1]["trials"] > reports[0]["trials"]
assert reports[2]["trials"] > reports[1]["trials"]
for r in reports:
    assert r["low"] <= r["estimate"] <= r["high"]
assert (reports[1]["high"] - reports[1]["low"]) < (reports[0]["high"] - reports[0]["low"])
assert (reports[2]["high"] - reports[2]["low"]) < (reports[1]["high"] - reports[1]["low"])
try:
    estimate_pi(0, seed=7)
except ValueError:
    pass
else:
    raise AssertionError("invalid trial count accepted")
print({"reports": reports, "target": math.pi, "seed": 7, "assumption": "independent uniform samples", "bias": "none for hit proportion under iid sampling", "limitation": "finite-sample error shrinks with sqrt(trials); model bias absent here"})