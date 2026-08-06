---
name: spacex-fsw
description: >-
  Write code like a flight-software team: run a bounded computation in three
  independent strings, reconcile by deterministic majority, expose one
  dissenter, and fail safe when no majority exists. Define a failure matrix for
  sensor loss, engine-out, and communications drop; keep memory bounded and
  remove branches that add failure surface without mission value. This skill is
  NOT for happy-path-only prototypes or real flight control without qualified
  engineering review. Triggers on: "spacex" "flight software" "fsw"
  "redundancy" "voting" "fault tolerance" "simulate" "rocket" "failure matrix"
  "triple redundant".
---

# SpaceX FSW Skill

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- three independent computations and deterministic majority reconciliation
- named handling for one dissenter and no-majority disagreement
- at least three exercised synthetic failure scenarios
- bounded memory/loops and no silent fallthrough
- one feature/branch removed with a stated failure-surface reason
- a safe result or explicit fault state for every matrix row

## Activation


You are a flight-software engineer.

Compute the mission-critical value three ways, compare the strings, and make the voting rule visible. A single dissent is masked but logged; no majority is a fault, never a guess. Define the synthetic failure matrix before the harness, keep loops and state bounded, and remove a feature that adds more failure surface than mission value. This is disciplined simulation, not certification.
## Core Principles

1. **Independent strings**: duplicated syntax is not independence; vary the route
   or source of the computation.
2. **Deterministic vote**: same inputs and faults yield the same result.
3. **No majority means safe fault**: never silently choose one string.
4. **Failure matrix first**: sensor loss, engine-out, and comms drop get explicit outcomes.
5. **Simplify the failure surface**: remove unneeded auto-tuning or hidden branches.

## Workflow

1. Define output invariant, fault model, and safe fallback.
2. Implement three bounded independent calculations.
3. Vote, log dissent, and fail closed when counts tie.
4. Run the failure matrix and assert each outcome.
5. Document the removed feature and why it was not worth its failure surface.

## Example Pattern

The vehicle commands a bounded thrust. Two agreeing strings mask one faulty
sensor; all-different strings enter a safe fault state. The feature `auto_tune`
is deliberately removed because it adds an unbounded state space to a fixed
mission envelope.

```python
def vote(strings):
    if not isinstance(strings, list) or len(strings) != 3 or any(not isinstance(value, int) or isinstance(value, bool) for value in strings):
        return {"status": "fault", "value": None, "agreement": 0, "dissent": [], "fault": True}
    counts = {value: strings.count(value) for value in strings}
    winner, agreement = max(counts.items(), key=lambda pair: pair[1])
    dissent = [value for value in strings if value != winner]
    return {"status": "ok" if agreement >= 2 else "fault", "value": winner if agreement >= 2 else None,
            "agreement": agreement, "dissent": dissent, "fault": agreement < 2}

def clamp(value):
    return max(0, min(100, value))

def mission(sensor, engine_out=False, comms_drop=False, sensor_loss=False):
    if not isinstance(sensor, int) or isinstance(sensor, bool) or not 0 <= sensor <= 100:
        return {"status": "fault", "value": None, "agreement": 0, "dissent": [], "fault": True}
    if sensor_loss:
        return {"status": "fault", "value": None, "agreement": 0, "dissent": [], "fault": True}
    # Independent strings: direct sensor, conservative average, and bounded table lookup.
    direct = clamp(sensor)
    average = clamp((sensor + (0 if engine_out else 2)) // 1)
    lookup = clamp([0, 20, 40, 60, 80, 100][sensor // 20])
    if comms_drop:
        lookup = clamp(lookup + 25)
    if engine_out:
        average = clamp(average - 2)
    return vote([direct, average, lookup])

matrix = {"sensor_loss": mission(40, sensor_loss=True), "engine_out": mission(40, engine_out=True), "comms_drop": mission(40, comms_drop=True), "triple_fault": vote([10, 20, 30])}
assert matrix["sensor_loss"]["status"] == "fault" and matrix["sensor_loss"]["fault"]
assert matrix["engine_out"]["status"] == "ok" and matrix["engine_out"]["dissent"] == [38]
assert matrix["comms_drop"]["status"] == "fault" and matrix["triple_fault"]["fault"]
assert vote([])["fault"] and mission("bad")["fault"]
print({"matrix": matrix, "removed": "auto_tune: unbounded failure surface"})
```

## Cross-Language Examples

The JavaScript and Rust blocks below are deliberately **voter-only reductions**;
the Python block is the full bounded scenario harness. They preserve the same
three-value vote/fault contract but do not pretend to reproduce every scenario
adapter in every language.

```javascript
function vote(values) { if (!Array.isArray(values) || values.length !== 3 || values.some(value => !Number.isInteger(value))) return { status: "fault", value: null, agreement: 0, dissent: [], fault: true }; const counts = new Map(values.map(value => [value, values.filter(other => other === value).length])); const winner = [...counts.entries()].sort((x, y) => y[1] - x[1])[0]; const dissent = values.filter(value => value !== winner[0]); return { status: winner[1] >= 2 ? "ok" : "fault", value: winner[1] >= 2 ? winner[0] : null, agreement: winner[1], dissent, fault: winner[1] < 2 }; }
const matrix = { sensorLoss: vote([40, 42, 40]), engineOut: vote([40, 38, 40]), commsDrop: vote([40, 42, 65]), tripleFault: vote([10, 20, 30]) };
if (matrix.engineOut.status !== "ok" || matrix.engineOut.dissent[0] !== 38 || matrix.commsDrop.status !== "fault" || matrix.tripleFault.status !== "fault" || !vote([]).fault) throw new Error("failure matrix failed");
console.log({ matrix, removed: "auto_tune: unbounded failure surface" });
```

```rust
fn vote(values: &[i32]) -> (&'static str, Option<i32>, usize, usize) {
    if values.len() != 3 { return ("fault", None, 0, values.len()); }
    let mut winner = values[0]; let mut agreement = 0;
    for candidate in values { let count = values.iter().filter(|other| **other == *candidate).count(); if count > agreement { winner = *candidate; agreement = count; } }
    (if agreement >= 2 { "ok" } else { "fault" }, if agreement >= 2 { Some(winner) } else { None }, agreement, values.iter().filter(|value| **value != winner).count())
}
fn main() {
    assert_eq!(vote(&[40, 42, 40]).0, "ok"); assert_eq!(vote(&[40, 38, 40]).3, 1);
    assert_eq!(vote(&[40, 42, 65]).0, "fault"); assert_eq!(vote(&[10, 20, 30]).0, "fault");
    println!("failure_matrix=sensor_loss engine_out comms_drop triple_fault removed=auto_tune");
}
```

## Safety

Do not deploy toy voters as flight control. Bound input, state, and retries;
log dissent without leaking sensitive telemetry; fail safe on disagreement; and
require domain experts, simulation, formal analysis, and certification for real
hardware.
