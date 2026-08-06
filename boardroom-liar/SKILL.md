---
name: boardroom-liar
description: >-
  A coding skill: Write the persuasive product story first, then turn every
  promise into a falsifiable claim with an owner, metric, baseline, sample,
  and deadline. Audit the implementation or proposal against those claims,
  label each supported, unsupported, or conditional, and rewrite the pitch with
  measured behavior and explicit limits. This skill is NOT for fabricating
  metrics or manipulating investors. Triggers on: "boardroom" "pitch" "founder"
  "audit the claims" "measurable behavior" "technical pitch"
  "persuasive explanation" "where that story is false" "falsifiable claim"
  "baseline and metric" "claim audit".
---

# Boardroom Liar Skill

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- the persuasive founder story written before the audit
- each material promise converted into a claim with metric, baseline, owner,
  sample/window, and falsifier
- evidence status for every claim: supported, unsupported, or conditional
- every unsupported claim rewritten as a limitation or measurement plan
- a final pitch that contains no stronger claim than the evidence supports

## Activation


You are a founder pitching the board, then the auditor who distrusts the slide.

Write the compelling story first without pretending it is true. Extract each promise into a claim ledger: what is measured, compared with which baseline, over what sample and time window, owned by whom, and what result would falsify it. Inspect implementation evidence, label claims supported/unsupported/conditional, and rewrite the story so its confidence matches the record. If there is no measurement, say “not measured”; do not fill the gap with a flattering number.
## Core Principles

1. **Rhetoric and evidence are separate artifacts**: preserve the original pitch
   so the audit can show exactly what changed.
2. **Claims need denominators**: “fast,” “scales,” and “users love it” are not
   metrics until baseline, population, and window are named.
3. **Unsupported is useful**: an honest measurement plan is better than a fake
   success claim.
4. **Falsifiers protect the board**: state what result would make the claim false
   before choosing a convenient result.
5. **Final language is bounded**: never let the rewrite regain certainty through
   adjectives the measurements do not warrant.

## Workflow

1. Write the pitch and mark every promise.
2. Build a claim ledger with metric, baseline, sample, window, owner, and
   falsifier.
3. Attach existing evidence; do not create evidence during the audit.
4. Classify each claim and identify gaps.
5. Rewrite the pitch with measured results, conditional language, and a concrete
   next measurement.

## Example Pattern

The original pitch says “infinitely scalable.” The ledger exposes the missing
capacity boundary and rewrites it into a measured, falsifiable statement.

```python
pitch = "Our system is fast, infinitely scalable, and loved by users."
claims = [
    {"text": "fast", "metric": "p95_ms", "baseline": 420, "observed": 180, "sample": 1000, "window": "load test", "owner": "perf", "falsifier": ">= baseline"},
    {"text": "infinitely scalable", "metric": "max_stable_rps", "baseline": None, "observed": 3000, "sample": 3, "window": "capacity steps", "owner": "infra", "falsifier": "any saturation"},
    {"text": "loved by users", "metric": "retention_30d", "baseline": None, "observed": None, "sample": 0, "window": "not measured", "owner": "product", "falsifier": "retention below target"},
]

def audit(claim):
    if claim["observed"] is None or claim["sample"] == 0:
        return {**claim, "status": "unsupported", "rewrite": f"{claim['text']} is not measured"}
    if claim["text"] == "fast":
        return {**claim, "status": "supported" if claim["observed"] < claim["baseline"] else "unsupported", "rewrite": f"p95 was {claim['observed']}ms vs {claim['baseline']}ms baseline"}
    return {**claim, "status": "conditional", "rewrite": f"stable through {claim['observed']} RPS in {claim['sample']} capacity steps"}

ledger = [audit(claim) for claim in claims]
assert [entry["status"] for entry in ledger] == ["supported", "conditional", "unsupported"]
assert ledger[2]["rewrite"] == "loved by users is not measured"
print({"original_pitch": pitch, "claim_ledger": ledger})
```

## Cross-Language Examples

```javascript
const pitch = "Our system is fast, infinitely scalable, and loved by users.";
const claims = [
  { text: "fast", metric: "p95_ms", baseline: 420, observed: 180, sample: 1000, window: "load test", owner: "perf", falsifier: ">= baseline" },
  { text: "infinitely scalable", metric: "max_stable_rps", baseline: null, observed: 3000, sample: 3, window: "capacity steps", owner: "infra", falsifier: "any saturation" },
  { text: "loved by users", metric: "retention_30d", baseline: null, observed: null, sample: 0, window: "not measured", owner: "product", falsifier: "retention below target" },
];
function audit(claim) {
  if (claim.observed === null || claim.sample === 0) return { ...claim, status: "unsupported", rewrite: `${claim.text} is not measured` };
  if (claim.text === "fast") return { ...claim, status: claim.observed < claim.baseline ? "supported" : "unsupported", rewrite: `p95 was ${claim.observed}ms vs ${claim.baseline}ms baseline` };
  return { ...claim, status: "conditional", rewrite: `stable through ${claim.observed} RPS in ${claim.sample} steps` };
}
const ledger = claims.map(audit);
if (ledger[2].status !== "unsupported" || ledger[0].status !== "supported") throw new Error("claim audit failed");
console.log({ pitch, ledger });
```

```rust
struct Claim {
    text: &'static str,
    metric: &'static str,
    baseline: Option<u32>,
    observed: Option<u32>,
    sample: u32,
    window: &'static str,
    owner: &'static str,
    falsifier: &'static str,
}
fn main() {
    let claim = Claim {
        text: "infinitely scalable", metric: "max_stable_rps", baseline: None,
        observed: Some(3000), sample: 3, window: "capacity steps", owner: "infra",
        falsifier: "any saturation",
    };
    let status = "conditional"; // bounded capacity test, not infinity
    assert_eq!(claim.observed, Some(3000));
    assert_eq!(status, "conditional");
    println!("claim={} metric={} status={} evidence={:?}rps/{}steps owner={} falsifier={}", claim.text, claim.metric, status, claim.observed, claim.sample, claim.owner, claim.falsifier);
}
```

## Safety

Never fabricate customer, performance, or financial evidence. Keep private
metrics access-controlled, distinguish measured facts from forecasts, and have
qualified reviewers inspect claims used in investor, safety, or compliance
materials.
