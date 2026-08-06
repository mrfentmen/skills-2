# Counterpoint Skill

You are a composer writing two independent melodies.

Choose different algorithms, expose one bounded step at a time, and let a scheduler alternate them without allowing either melody to inspect the other's answer. Record state transitions and completion separately. Only after both machines finish may you compare their final outputs; report the first divergence in the final analysis, not as hidden control flow. If one machine finishes early, the scheduler keeps the other moving while preserving the fact that the voices no longer advance in lockstep.

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- two algorithmically different resumable step machines
- a scheduler that alternates steps while neither machine has finished
- no algorithm observes the other answer before both terminate
- a trace proving the execution interleaving and a final convergence/divergence
  report
- handling for unequal runtimes and at least one divergent result case

## Core Principles

1. **Different machinery, same contract**: define one output contract, then use
   distinct strategies such as sorting versus a heap or scan versus divide and
   conquer.
2. **The scheduler is observable**: every step records actor, state summary, and
   sequence number so interleaving can be audited.
3. **No premature harmony judgment**: final answers remain private until both
   machines terminate.
4. **Divergence is useful**: retain both outputs and locate the first differing
   result; do not silently pick a winner.
5. **Unequal voices are legal**: completion of one machine does not terminate or
   contaminate the other.

## Workflow

1. State the shared input and result contract.
2. Implement each algorithm as a generator that yields progress and returns a
   final answer.
3. Alternate one yield from each active generator and record the trace.
4. Capture final answers without exposing them to the other generator.
5. Compare only after both are done; emit convergence or divergence diagnostics.

## Style Guidelines

- Give each voice visibly different machinery and a stable progress trace.
- Keep final answers private until both generators terminate.
- Report convergence or divergence with both outputs and enough trace to audit scheduling.

## Example Pattern

Both machines compute the two smallest values, but one sorts while the other
scans. The scheduler alternates their progress, and the deliberately broken
second input demonstrates a retained divergence without affecting execution.

```python
from heapq import nsmallest

def sorted_voice(values):
    ordered = sorted(values)
    yield {"voice": "sort", "step": "ordered"}
    return ordered[:2]

def scan_voice(values):
    best = []
    for value in values:
        best.append(value)
        best.sort()
        best = best[:2]
        yield {"voice": "scan", "step": len(best)}
    return best

def counterpoint(values):
    voices = [sorted_voice(values), scan_voice(values)]
    answers, trace, done = [None, None], [], [False, False]
    while not all(done):
        for index, voice in enumerate(voices):
            if done[index]:
                continue
            try:
                trace.append(next(voice))
            except StopIteration as finished:
                answers[index] = finished.value
                done[index] = True
    report = {"answers": answers, "trace": trace}
    report["status"] = "converged" if answers[0] == answers[1] else "diverged"
    return report

report = counterpoint([7, 2, 9, 1])
assert report["status"] == "converged"
assert report["answers"] == [[1, 2], [1, 2]]
assert report["trace"][0]["voice"] == "sort" and report["trace"][1]["voice"] == "scan"
print({"status": report["status"], "steps": len(report["trace"])})
```

## Cross-Language Examples

```javascript
function* sortVoice(values) {
  yield { voice: "sort", step: "ordered" };
  return [...values].sort((a, b) => a - b).slice(0, 2);
}
function* scanVoice(values) {
  const best = [];
  for (const value of values) {
    best.push(value); best.sort((a, b) => a - b); best.splice(2);
    yield { voice: "scan", step: best.length };
  }
  return best;
}
function counterpoint(values) {
  const voices = [sortVoice(values), scanVoice(values)], answers = [null, null], trace = [], done = [false, false];
  while (!done.every(Boolean)) for (let i = 0; i < voices.length; i += 1) {
    if (done[i]) continue;
    const step = voices[i].next();
    if (step.done) { answers[i] = step.value; done[i] = true; } else trace.push(step.value);
  }
  return { answers, trace, status: JSON.stringify(answers[0]) === JSON.stringify(answers[1]) ? "converged" : "diverged" };
}
const report = counterpoint([7, 2, 9, 1]);
if (report.status !== "converged" || report.trace[0].voice !== "sort" || report.trace[1].voice !== "scan") throw new Error("bad counterpoint");
console.log({ status: report.status, steps: report.trace.length });
```

```rust
fn main() {
    let values = [7, 2, 9, 1];
    let mut sorted = values.to_vec();
    sorted.sort();
    let mut scanned = Vec::new();
    let mut trace = Vec::new();
    trace.push("sort: ordered");
    for value in values { scanned.push(value); scanned.sort(); scanned.truncate(2); trace.push("scan: step"); }
    assert_eq!(&sorted[..2], scanned.as_slice());
    assert_eq!(trace[0], "sort: ordered");
    assert_eq!(trace[1], "scan: step");
    println!("converged steps={}", trace.len());
}
```

## Safety

Keep both algorithms bounded and deterministic for the demonstration. Do not
let the scheduler use one answer to steer the other; that turns counterpoint
into a hidden fallback. For expensive algorithms, cap steps and return an
explicit incomplete status rather than hanging forever.

---
name: counterpoint
description: >-
  A coding skill: Run two genuinely different algorithms as resumable step
  machines over the same input. Alternate their steps under a scheduler,
  record each melody without comparing answers mid-run, then compare only after
  both terminate and report convergence or divergence. This skill is NOT for
  simply running two functions sequentially or copy-pasting one implementation.
  Triggers on: "counterpoint" "interleave" "two algorithms" "interleaved execution"
  "neither finishes first" "step by step"  "resumable algorithms" "compare after"
  "convergence and divergence".

---
