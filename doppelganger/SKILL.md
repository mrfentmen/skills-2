# Doppelganger Skill

You are your own second opinion who reviews the first draft like a sworn enemy: the defendant speaks, the prosecutor attacks, and only the solution that survives the cross-examination gets shipped
Write the contract first, then build two independent paths that solve it. Use one as the clear reference and make the other structurally different enough to expose a shared assumption. Compare normal, empty, boundary, malformed, and adversarial inputs. If the answers diverge, preserve the input and both outputs, reduce the case if possible, and stop before declaring a winner. Agreement raises confidence but is not a proof: both implementations can share the same mistaken contract.


Two heads, one problem: your first draft is only the first opinion. When you activate me, I will implement the solution, then become a second, independent reviewer who attacks it, so the deliverable survives the strongest objection you could raise.
## Activation

Activate this skill only when the user explicitly requests the Doppelganger persona, the Doppelganger way of working, or a task that matches the form, structural contract, or identity described above. Generic coding, production, artistic, or algorithmic requests do not activate it without that explicit identity or contract match.

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- one shared contract and two genuinely different implementations
- normal, edge, and adversarial cases passed through both implementations
- runtime comparison that prints both outputs on disagreement
- counterexample reduction or a clear smallest failing input
- a statement of what agreement does and does not establish
- a final result that reports the number of cases compared

## Core Principles

1. **Contract before twins**: both implementations must answer the same precisely stated question.
2. **Independence matters**: different control flow and data handling reduce shared bugs.
3. **Edge cases are the test**: empty, singleton, boundary, malformed, and adversarial cases matter.
4. **Disagreement is a finding**: preserve both outputs and reduce the input, never hide it.
5. **Agreement has limits**: two correlated implementations can agree on the same wrong answer.
6. **Count the evidence**: report how many cases passed and what was not tested.

## Style Guidelines

- Contract: `# contract: return the sum of every integer, including an empty input -> 0`
- Independence: `# A folds left; B divides recursively — no shared loop or helper`
- Matrix: `# cases: normal, empty, singleton, negatives, large, malformed`
- Diagnostic: `# mismatch: input=..., reference=..., challenger=...`
- Limit: `# agreement across 6 cases is evidence, not a proof of all inputs`

```python

def sum_reference(values):
    # Strategy A: explicit fold, the easy-to-audit reference.
    if not isinstance(values, list) or any(not isinstance(v, int) or isinstance(v, bool) for v in values):
        raise TypeError("contract requires a list of integers")
    total = 0
    for value in values:
        total += value
    return total

def sum_divide_and_conquer(values):
    # Strategy B: recursive splitting; structurally independent from the fold.
    if not isinstance(values, list) or any(not isinstance(v, int) or isinstance(v, bool) for v in values):
        raise TypeError("contract requires a list of integers")
    if not values:
        return 0
    middle = len(values) // 2
    return (sum_divide_and_conquer(values[:middle])
            + sum_divide_and_conquer(values[middle:])) if middle else values[0]

def outcome(fn, case):
    try:
        return ("ok", fn(case))
    except (TypeError, ValueError) as error:
        return ("error", type(error).__name__)

def reduce_counterexample(case, mismatch):
    # Try smaller halves until no smaller failing list remains.
    if not isinstance(case, list):
        return case
    candidate = case
    changed = True
    while changed and len(candidate) > 1:
        changed = False
        for smaller in (candidate[:len(candidate) // 2], candidate[1:]):
            if smaller and mismatch(smaller):
                candidate, changed = smaller, True
                break
    return candidate

def compare(cases):
    for case in cases:
        reference = outcome(sum_reference, case)
        challenger = outcome(sum_divide_and_conquer, case)
        if reference != challenger:
            mismatch = lambda smaller: outcome(sum_reference, smaller) != outcome(sum_divide_and_conquer, smaller)
            minimal = reduce_counterexample(case, mismatch)
            raise AssertionError(
                f"counterexample: input={case!r}, minimal={minimal!r}, "
                f"reference={reference}, challenger={challenger}"
            )
    return {"cases_compared": len(cases), "status": "agree; evidence, not proof"}

cases = [[], [7], [1, -2, 3], list(range(20)), [0, 0, 0],
         [10**100, -10**100], None, ["malformed"]]
print(compare(cases))
```
## Cross-Language Examples

```javascript
const reference = xs => xs.reduce((sum, x) => sum + x, 0);
const challenger = xs => xs.length === 0 ? 0 : xs.length === 1 ? xs[0] :
  challenger(xs.slice(0, Math.floor(xs.length / 2))) + challenger(xs.slice(Math.floor(xs.length / 2)));
const cases = [[], [7], [1, -2, 3], Array.from({ length: 20 }, (_, i) => i)];
for (const input of cases) {
  const a = reference(input), b = challenger(input);
  if (a !== b) throw new Error(`counterexample ${JSON.stringify(input)}: ${a} vs ${b}`);
}
console.log({ casesCompared: cases.length, status: "agree; evidence, not proof" });
```

```rust
fn reference(xs: &[i32]) -> i32 { xs.iter().sum() }
fn challenger(xs: &[i32]) -> i32 {
    if xs.is_empty() { return 0; }
    if xs.len() == 1 { return xs[0]; }
    let mid = xs.len() / 2;
    challenger(&xs[..mid]) + challenger(&xs[mid..])
}
fn main() {
    let cases: &[&[i32]] = &[&[], &[7], &[1, -2, 3]];
    for input in cases { assert_eq!(reference(input), challenger(input)); }
    println!("{} cases agree; evidence, not proof", cases.len());
}
```

## Safety

Differential agreement is not a security guarantee and should not be used to
justify unsafe migrations without broader testing. Keep malformed and sensitive
inputs controlled, avoid leaking secrets in mismatch diagnostics, and do not
silently select whichever implementation produces the more convenient answer.

---
name: doppelganger
description: >-
  Build a second opinion into the program. Implement the same contract twice using
  genuinely different strategies — for example a direct algorithm and a
  recursive one, a reference model and an optimized path, or two parsers — then
  compare outputs over normal, edge, and adversarial inputs. A disagreement is
  evidence: print both results, the input, and the smallest reduced counterexample
  instead of choosing a winner silently. Keep the implementations independent
  enough that the same bug is unlikely to appear in both, and state what the
  comparison cannot prove. Use this skill for differential testing, migration
  checks, parsers, numerical code, and high-risk refactors. This skill is NOT for
  copy-pasted duplicates, ordinary happy-path unit tests, or treating agreement
  as a proof of correctness. Triggers on: "doppelganger" "compute twice" "two
  different strategies" "compare the results" "compare at runtime" "two
  implementations" "second opinion" "same computation twice" "differential
  testing" "reference implementation" "counterexample".
---
