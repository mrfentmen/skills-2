---
name: oracle
description: >-
  Make predictions like a careful oracle: state a falsifiable belief before
  gathering evidence, define what observation would confirm or disconfirm it,
  collect a real sample or measurement, then revise the belief with an explicit
  confidence and uncertainty label. Separate prior, evidence, likelihood, and
  judgment so the final answer does not pretend that a noisy probe is certainty.
  Keep a prediction ledger over time: record calibration, false positives, false
  negatives, and what evidence changed the conclusion. Use this skill for
  classifiers, simulations, searches, diagnostics, and forecasting. This skill
  is NOT for prophecy, post-hoc storytelling, or presenting an underpowered
  sample as fact. Triggers on: "oracle" "prediction" "gather evidence" "revise
  the prediction" "initial belief" "final judgment" "state your belief"
  "falsifiable prediction" "confidence" "calibration" "prediction ledger"
  "evidence changed my mind".
---

# Oracle Skill

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- a prediction stated before evidence, with a confidence or prior
- a falsifier: the observation that would change or reject the prediction
- a real probe with sample size, observed evidence, and limitations
- an updated judgment that labels uncertainty instead of claiming certainty
- a calibration or ledger entry that can be checked against later outcomes

## Activation


You are the oracle: state your belief, gather evidence, revise it.

A prediction is not a performance of certainty; it is a claim exposed to a possible future observation. Write the prior and the falsifier before looking at the data. Use a probe that could actually change your mind, count the sample, and distinguish signal from noise. Update the judgment with an explicit confidence and limitation, then record the prediction so a later outcome can score your calibration.
## Core Principles

1. **Prediction before perception**: do not write the story after seeing the result.
2. **Falsifier before confidence**: name what would make the belief lose.
3. **Evidence must have a probe**: observation is collected, not asserted.
4. **Update proportionally**: one noisy sample should not create absolute certainty.
5. **Record the call**: a ledger makes future calibration possible.
6. **A wrong oracle is useful**: false predictions teach where the model is weak.

## Style Guidelines

- Prior: `# prior: cache is cold, confidence=0.60`
- Falsifier: `# falsifier: >= 8/10 fast responses would make warm more likely`
- Probe: `# probe: measure 10 response times; threshold fixed before reading them`
- Update: `# evidence: 2/10 fast; posterior label=cold, confidence=0.75`
- Limitation: `# limitation: ten observations cannot establish production-wide behavior`
- Ledger: `# call_id=cache-001; prediction=cold; outcome=pending; score later`

```python

def oracle_call(observations, threshold=0.30):
    # Prior and falsifier are fixed before looking at observations.
    prior = {"label": "cold", "confidence": 0.60}
    falsifier = f"evidence >= {threshold:.2f} would favor warm"
    evidence = sum(observations) / len(observations) if observations else None
    if evidence is None:
        judgment = {"label": "unknown", "confidence": 0.0}
    else:
        label = "cold" if evidence < threshold else "warm"
        # This is a small-sample heuristic, not a calibrated probability.
        confidence = min(0.95, 0.50 + abs(evidence - threshold))
        judgment = {"label": label, "confidence": round(confidence, 2)}
    ledger = {"call_id": "cache-001", "prediction": prior["label"],
              "evidence_n": len(observations), "falsifier": falsifier,
              "judgment": judgment, "outcome": "pending"}
    return ledger

# 1 means fast/warm; 0 means slow/cold. The threshold was fixed beforehand.
print(oracle_call([0, 0, 1, 0, 0, 0, 0, 0, 0, 0]))
```

## Cross-Language Examples

```javascript
const oracleCall = (observations, threshold = 0.3) => {
  const evidence = observations.length ? observations.reduce((a, b) => a + b, 0) / observations.length : null;
  const label = evidence === null ? "unknown" : evidence < threshold ? "cold" : "warm";
  return { prediction: "cold", evidenceN: observations.length, label, confidence: evidence === null ? 0 : 0.5 + Math.abs(evidence - threshold) };
};
console.log(oracleCall([0, 0, 1, 0, 0]));
```

```rust
fn main() {
    let observations = [0u32, 0, 1, 0, 0];
    let warm = observations.iter().sum::<u32>() as f64 / observations.len() as f64;
    let label = if warm < 0.3 { "cold" } else { "warm" };
    println!("prediction=cold evidence_n={} judgment={}", observations.len(), label);
}
```

## Safety

Predictions about people, health, finances, or safety require stronger evidence,
privacy protections, and qualified judgment than this toy workflow provides.
Never turn a confidence label into a guarantee, hide the sample size, or use
sensitive data without authorization. Keep the prediction ledger honest: a wrong
call remains wrong, and updating the story after the outcome is not calibration.
