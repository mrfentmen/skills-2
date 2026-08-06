---
name: trial-by-combat
description: >-
  A coding skill: Put two independent implementations under the same executable
  challenge corpus. Score correctness, invariant violations, and resource cost
  with a declared deterministic rule; accept a winner only when it passes the
  contract, preserve both diagnostics, and discard neither evidence nor a
  failing challenger prematurely. Use this for adversarial algorithms and
  competitive computation. This skill is NOT for ordinary A/B testing. Triggers
  on: "trial by combat" "competing implementations" "fight" "champion"
  "winner takes the state" "deterministic rule" "challenge corpus"
  "score the implementations" "contract gate" "winner diagnostics".
---

# Trial By Combat Skill

You are the referee, not a fan.

Define the shared contract and challenge corpus before running either implementation. Each challenger runs independently against normal, boundary, malformed, and adversarial cases; correctness and invariants are gates, not points that speed can compensate for. Apply a declared lexicographic rule—first contract failures, then measured cost, then stable name as tie-break—and report both fighters' evidence. The winner may own the final state, but the loser's failures remain part of the audit trail.

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- two genuinely different implementations with a shared input/output contract
- a challenge corpus containing normal, edge, and adversarial cases
- independent result and invariant checks for each challenger
- a deterministic score and tie-break rule declared before the fight
- a final winner only among contract-passing challengers
- diagnostics for both winner and loser, including failed cases and cost

## Core Principles

1. **Same arena, same contract**: inputs, output shape, invalid-input policy, and
   oracle are identical for both challengers.
2. **Correctness before speed**: a fast implementation with a contract failure
   cannot win; scoring happens only after validity is established.
3. **Deterministic combat**: score and tie-breaks are fixed before execution so
   reruns do not rewrite history.
4. **Evidence survives the fight**: keep per-case outputs, failures, and costs;
   never hide a losing challenger that exposed a bug.
5. **Winner is scoped**: victory means best under this corpus and metric, not
   universal proof of superiority.

## Workflow

1. Write the operation contract, invalid-input behavior, and independent oracle.
2. Create a fixed challenge corpus covering ordinary, empty, duplicate, boundary,
   and malformed inputs.
3. Run each implementation in isolation and collect output, validity, and cost.
4. Reject any challenger with a contract or invariant failure.
5. Among survivors, choose by declared cost and stable name tie-break.
6. Publish the winner plus complete loser diagnostics and corpus limitations.

## Example Pattern

Both fighters implement `unique_sorted`: sorted output with duplicates removed;
malformed inputs are rejected. Correctness is gated first, then comparison count
wins. The example includes a deliberately broken fighter to show that speed or
style cannot rescue a contract failure.

```python
def bubble_unique(values):
    if not isinstance(values, list) or not all(isinstance(x, int) for x in values):
        raise TypeError("list[int] required")
    work = list(values)
    comparisons = 0
    for end in range(len(work) - 1, 0, -1):
        for i in range(end):
            comparisons += 1
            if work[i] > work[i + 1]:
                work[i], work[i + 1] = work[i + 1], work[i]
    return list(dict.fromkeys(work)), comparisons

def broken_unique(values):
    if not isinstance(values, list) or not all(isinstance(x, int) for x in values):
        raise TypeError("list[int] required")
    return values, 0                 # fast, but duplicates violate the contract

def oracle(values):
    return sorted(set(values))

def judge(fighter, cases):
    failures, cost = [], 0
    for case in cases:
        expected_rejection = not isinstance(case, list) or not all(isinstance(x, int) for x in case)
        try:
            result, spent = fighter(case)
            cost += spent
            if expected_rejection:
                failures.append({"case": repr(case), "reason": "invalid input was accepted"})
            elif result != oracle(case):
                failures.append({"case": case, "reason": "wrong result", "actual": result})
        except (TypeError, ValueError) as exc:
            if not expected_rejection:
                failures.append({"case": case, "reason": f"unexpected rejection: {exc}"})
        except Exception as exc:
            failures.append({"case": repr(case), "reason": f"unexpected: {exc}"})
    return {"failures": failures, "cost": cost, "valid": not failures}

cases = [[], [3, 1, 3, 2], [0], [-2, -2], "not-a-list"]
score_a = judge(bubble_unique, cases)
score_b = judge(broken_unique, cases)
scores = {"bubble": score_a, "broken": score_b}
champion = min(
    (name for name, score in scores.items() if score["valid"]),
    key=lambda name: (scores[name]["cost"], name),
)
assert champion == "bubble"
assert not score_b["valid"]
print({"champion": champion, "scores": scores})
```

## Cross-Language Examples

```javascript
function bubbleUnique(values) {
  if (!Array.isArray(values) || values.some(Number.isNaN)) throw new TypeError("number array required");
  const work = [...values]; let comparisons = 0;
  for (let end = work.length - 1; end > 0; end -= 1)
    for (let i = 0; i < end; i += 1) { comparisons += 1; if (work[i] > work[i + 1]) [work[i], work[i + 1]] = [work[i + 1], work[i]]; }
  return { result: [...new Set(work)], comparisons };
}
function judge(fighter, cases) {
  const failures = []; let cost = 0;
  for (const input of cases) {
    try { const actual = fighter(input); cost += actual.comparisons; const expected = [...new Set(input)].sort((a, b) => a - b); if (JSON.stringify(actual.result) !== JSON.stringify(expected)) failures.push({ input, reason: "wrong result" }); }
    catch (error) { if (Array.isArray(input)) failures.push({ input, reason: error.message }); }
  }
  return { failures, cost, valid: failures.length === 0 };
}
const cases = [[], [3, 1, 3, 2], [0], [-2, -2]];
const score = judge(bubbleUnique, cases);
if (!score.valid || score.failures.length) throw new Error("valid challenger lost");
console.log({ champion: "bubble", score });
```

```rust
fn unique_sorted(mut values: Vec<i32>) -> (Vec<i32>, usize) {
    let mut comparisons = 0;
    for end in (1..values.len()).rev() {
        for i in 0..end {
            comparisons += 1;
            if values[i] > values[i + 1] { values.swap(i, i + 1); }
        }
    }
    values.dedup();
    (values, comparisons)
}
fn main() {
    let (result, cost) = unique_sorted(vec![3, 1, 3, 2]);
    assert_eq!(result, vec![1, 2, 3]);
    println!("champion=bubble cost={}", cost);
}
```

## Safety

Do not run untrusted challengers in the same privileged process or let a test
corpus contain destructive inputs. Use timeouts, resource limits, and process
isolation for real adversarial code. A winner is not a security certification;
report coverage and corpus limits honestly.
