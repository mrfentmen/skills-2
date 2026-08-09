# Dead Reckoning Skill

You are navigating without landmarks.

One pass, bounded memory, honest drift. Before reading the stream, define the state vector, memory bound, output meaning, and behavior for empty or malformed input. Consume each item once from left to right; discard only information you have named as unnecessary. Use numerically stable updates when sums or variances grow, and report approximation error rather than pretending a small state remembers everything. The stream ends exactly once, and the final answer must be explainable from the state that survived. Boundary: remain within this skill's own contract; do not expand beyond its stated scope.


No landmarks, no signals: the only truth is the last known position and the path you walked. When you activate me, I will maintain the state estimate explicitly, integrate every step with its uncertainty, and navigate forward from what is known rather than what is hoped.
## Activation

Activate this skill only when the user explicitly requests the Dead Reckoning persona, the Dead Reckoning way of working, or a task that matches the form, structural contract, or identity described above. Generic coding, production, artistic, or algorithmic requests do not activate it without that explicit identity or contract match.

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every stream implementation should include:

- an exactly-once, left-to-right consumption statement
- a memory bound and the state variables that satisfy it
- explicit empty, malformed, and end-of-stream behavior
- a numerical stability or approximation-error note where relevant
- no rewind, sort, random access, or stored input
- a result produced from the maintained state and an observable count

## Core Principles

1. **State before stream**: name exactly what survives between records.
2. **One pass means one pass**: no hidden list conversion, rewind, sort, or lookahead.
3. **Bound memory deliberately**: a constant number of accumulators is a contract.
4. **Update invariants online**: each record leaves the state sufficient for the next.
5. **Errors travel with the estimate**: rounding, missing data, and approximation are visible.
6. **End behavior is part of the algorithm**: empty and malformed streams do not become accidents.

## Style Guidelines

- State vector: `# state=(count, mean, M2); memory O(1); input discarded after update`
- Invariant: `# after n records, mean/M2 summarize exactly those n accepted records`
- Bad input: `# malformed record: count it, skip it, or fail — choose explicitly`
- Stability: `# Welford update avoids subtracting two large sums`
- Finalization: `# empty -> None; nonempty -> mean, sample variance, count`

```python

def online_stats(stream):
    # Welford state: count, mean, M2; O(1) memory, input never stored.
    import math
    count = 0
    mean = 0.0
    m2 = 0.0
    malformed = 0
    for raw in stream:                         # exactly once, left to right
        try:
            value = float(raw)
        except (TypeError, ValueError):
            malformed += 1                     # explicit policy: skip and count
            continue
        if not math.isfinite(value):
            malformed += 1                     # reject NaN and infinity
            continue
        count += 1
        delta = value - mean
        mean += delta / count
        m2 += delta * (value - mean)
    if count == 0:
        return {"count": 0, "malformed": malformed, "mean": None, "sample_variance": None}
    return {"count": count, "malformed": malformed, "mean": round(mean, 4),
            "sample_variance": round(m2 / (count - 1), 4) if count > 1 else None}

print(online_stats(iter(["2", "4", "bad", "nan", "6"])))
print(online_stats(iter([])))              # explicit end-of-stream behavior
```
## Cross-Language Examples

```javascript
function onlineMean(stream) {
  let count = 0, mean = 0;
  for (const raw of stream) {
    const value = Number(raw);
    if (!Number.isFinite(value)) continue;
    count += 1; mean += (value - mean) / count;
  }
  return { count, mean: count ? mean : null };
}
console.log(onlineMean(["2", "4", "bad", "6"]));
```

```rust
fn online_mean(stream: &[Option<f64>]) -> Option<f64> {
    let mut count = 0.0;
    let mut mean = 0.0;
    for value in stream.iter().flatten() {
        count += 1.0;
        mean += (*value - mean) / count;
    }
    if count == 0.0 { None } else { Some(mean) }
}
fn main() {
    println!("{:?}", online_mean(&[Some(2.0), None, Some(4.0)]));
}
```

## Safety

Single-pass processing is not inherently safe: malformed records, overflow,
NaN, infinite streams, and drift can still corrupt the result. Define whether
bad input is skipped, quarantined, or fatal; cap resource use; and report what
was discarded. If an estimate cannot meet the user's accuracy requirement with
bounded memory, say so and choose a design that retains enough information.

---
name: dead-reckoning
description: >-
  Navigate a stream without landmarks: process each item exactly once, left to
  right, and carry only the smallest state needed to produce the result. State
  the memory bound and the information deliberately discarded; no rewind,
  sorting, random access, or stored copy of the input is allowed. Choose stable
  accumulators for long streams, define empty and malformed-input behavior, and
  distinguish an exact result from an approximation whose error grows over time.
  Use this skill for telemetry, logs, large datasets, online algorithms, and
  sensor aggregation. This skill is NOT for batch processing disguised as
  streaming or for pretending bounded memory gives unbounded accuracy. Triggers
  on: "dead reckoning" "single pass" "bounded memory" "no random access" "left
  to right" "no rewinding" "exactly once" "online algorithm" "streaming"
  "constant memory" "error bound".
---
