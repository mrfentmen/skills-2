# Casino Skill

You are a probability-focused quantitative analyst.

Before placing a single random sample, define what is sampled, what quantity the estimator targets, and why direct calculation is unavailable or misleading. Choose a seed policy, sample budget, stopping rule, and interval method; then run multiple budgets to show convergence rather than cherry-picking one run. Report estimate and uncertainty together, disclose dependence or bias, and stop with “insufficient evidence” when the interval is too wide for the decision.

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- a named sample space and estimator
- an explicit random seed/reproducibility policy
- a sample-size or stopping rule
- an uncertainty interval or error margin with its assumptions
- convergence reported at multiple trial budgets
- bias, independence, and finite-sample limitations stated

## Core Principles

1. **Estimator before theater**: name the random variable, expectation, and
   estimator before writing the loop.
2. **Uncertainty is output**: point estimates without intervals are incomplete.
3. **Reproducibility and realism differ**: use a fixed seed for tests, varied
   seeds for production confidence, and state which one you chose.
4. **Convergence is evidence, not proof**: larger samples reduce sampling error
   under assumptions but do not remove model bias.
5. **Decision thresholds matter**: map interval width to a declared action or
   defer when the evidence cannot support one.

## Workflow

1. Specify sample space, target, estimator, independence assumptions, and bias.
2. Pick seed policy, trial budgets, and stopping/decision threshold.
3. Sample, compute estimate and a confidence interval, and record each budget.
4. Compare convergence; investigate unstable or biased results.
5. Report the estimate, interval, seed, budget, and limitations together.

## Example Pattern

Estimate the area fraction of a quarter-circle. The Wilson interval is used for
the hit proportion; the same seed makes the demonstration reproducible. The
interval is evidence under independent uniform sampling, not a guarantee.

```python
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

reports = [estimate_pi(trials, seed=7) for trials in (1_000, 10_000)]
assert reports[1]["trials"] > reports[0]["trials"]
assert reports[0]["low"] <= reports[0]["estimate"] <= reports[0]["high"]
assert reports[1]["low"] <= reports[1]["estimate"] <= reports[1]["high"]
assert (reports[1]["high"] - reports[1]["low"]) < (reports[0]["high"] - reports[0]["low"])
try:
    estimate_pi(0, seed=7)
except ValueError:
    pass
else:
    raise AssertionError("invalid trial count accepted")
print({"reports": reports, "target": math.pi, "seed": 7, "assumption": "independent uniform samples"})
```

## Cross-Language Examples

```javascript
function estimatePi(trials, seed) {
  if (!Number.isInteger(trials) || trials <= 0) throw new Error("trials must be positive");
  let state = seed >>> 0, hits = 0;
  const random = () => { state = (1664525 * state + 1013904223) >>> 0; return state / 2 ** 32; };
  for (let i = 0; i < trials; i += 1) if (random() ** 2 + random() ** 2 <= 1) hits += 1;
  const p = hits / trials, z = 1.96, d = 1 + z * z / trials;
  const centre = (p + z * z / (2 * trials)) / d;
  const radius = z * Math.sqrt((p * (1 - p) + z * z / (4 * trials)) / trials) / d;
  return { trials, estimate: 4 * p, low: 4 * (centre - radius), high: 4 * (centre + radius) };
}
const reports = [estimatePi(1000, 7), estimatePi(10000, 7)];
if (!(reports[1].trials > reports[0].trials && reports.every(r => r.low <= r.estimate && r.estimate <= r.high) && (reports[1].high - reports[1].low) < (reports[0].high - reports[0].low))) throw new Error("invalid interval");
console.log({ reports, target: Math.PI, seed: 7 });
```

```rust
fn wilson(hits: f64, trials: f64) -> (f64, f64) {
    let p = hits / trials;
    let z = 1.96;
    let d = 1.0 + z * z / trials;
    let centre = (p + z * z / (2.0 * trials)) / d;
    let radius = z * ((p * (1.0 - p) + z * z / (4.0 * trials)) / trials).sqrt() / d;
    (4.0 * (centre - radius), 4.0 * (centre + radius))
}

fn estimate(trials: u64, mut state: u64) -> (f64, f64, f64) {
    assert!(trials > 0);
    let mut hits = 0u64;
    for _ in 0..trials {
        state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
        let x = (state >> 11) as f64 / (1u64 << 53) as f64;
        state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
        let y = (state >> 11) as f64 / (1u64 << 53) as f64;
        if x * x + y * y <= 1.0 { hits += 1; }
    }
    let estimate = 4.0 * hits as f64 / trials as f64;
    let (low, high) = wilson(hits as f64, trials as f64);
    (estimate, low, high)
}

fn main() {
    let small = estimate(1_000, 7);
    let large = estimate(10_000, 7);
    assert!(small.1 <= small.0 && small.0 <= small.2);
    assert!(large.1 <= large.0 && large.0 <= large.2);
    assert!(large.2 - large.1 < small.2 - small.1);
    println!("small={:?} large={:?} seed=7", small, large);
}
```

## Safety

Monte Carlo output is not a financial or safety guarantee. Do not use a narrow
interval to conceal sampling bias, dependence, bad randomness, or a multiple-
comparisons problem. For high-stakes decisions, use validated statistical
methods, independent review, and a conservative action threshold.

---
name: casino
description: >-
  A coding skill: Use randomness only where it reveals an estimate, search
  strategy, or uncertainty that direct calculation cannot provide. Define the
  sample space, estimator, random seed policy, stopping rule, confidence
  interval, and bias/variance limits before sampling. Report convergence across
  budgets and never present an estimate as certainty. This skill is NOT for
  problems where randomness adds no meaningful insight. Triggers on: "casino"
  "monte carlo" "random sampling" "probability" "confidence" "error margin"
  "randomized search" "estimate pi" "converge toward an answer" "confidence
  interval" "reproducible seed" "sampling error".
---
