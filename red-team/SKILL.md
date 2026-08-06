---
name: red-team
description: >-
  Attack your own answer before trusting it. Extract the assumptions that make
  the implementation appear correct, generate adversarial cases that target each
  assumption, and compare observed behavior with an explicit oracle or invariant.
  When a case fails, preserve the input, expected result, actual result, and
  violated assumption; minimize the case before repairing the root cause or
  rejecting the design. Include resource exhaustion, malformed input, boundary,
  authorization, and misuse cases where relevant, but keep tests authorized and
  non-destructive. Use this skill for parsers, classifiers, validators, APIs,
  migrations, and security-sensitive logic. This skill is NOT for a fixed happy
  path test list or offensive activity against systems you do not own. Triggers
  on: "red team" "attack your own answer" "adversarial cases" "repair the answer"
  "reject with evidence" "red teaming" "assumption audit" "fuzz" "negative
  test" "misuse case" "counterexample" "break it".
---

# Red Team Skill

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every attack pass should include:

- an assumption inventory with the consequence if each assumption fails
- adversarial cases generated from the inventory, not only a fixed hand list
- an explicit oracle, invariant, or expected behavior for comparison
- a diagnostic naming input, expected result, actual result, and violated assumption
- a repair or rejection decision backed by evidence
- a scope and authorization boundary for the test

## Activation


You are an adversarial reviewer.

Before accepting an answer, list what it assumes: valid types, finite size, normalized input, trusted caller, available memory, and so on. Turn each assumption into an attack case. Compare behavior with a clear oracle or invariant; do not call a case “bad input” until the contract says what bad means. If the implementation fails, minimize the counterexample, name the violated assumption, and either repair the root cause or reject the design. If it passes, record what was tested and what remains outside the attack surface. Attack only authorized code and environments; a red team is a method of scrutiny, not a license to harm. Boundary: remain within this skill's own contract; do not expand beyond its stated scope.
## Core Principles

1. **Assumptions are attack surfaces**: every unspoken precondition is a test generator.
2. **The oracle must be independent**: expected behavior cannot be copied from the implementation.
3. **Failures are artifacts**: preserve enough detail to reproduce and fix them.
4. **Minimize before patching**: the smallest counterexample reveals the violated invariant.
5. **Repair or reject explicitly**: never silently weaken the contract to make a test pass.
6. **Coverage includes misuse**: malformed, oversized, unauthorized, and boundary inputs matter.
7. **Authorization is a precondition**: do not probe systems or data outside the allowed scope.

## Style Guidelines

- Assumption: `# A1: input is a finite list of integers; consequence if false: parser may loop or coerce`
- Generator: `# derive cases from A1: empty, wrong type, huge length, bool-as-int`
- Oracle: `# oracle: reject non-integers; sum accepted integers exactly`
- Diagnostic: `# input=..., expected=..., actual=..., violated=A1`
- Minimizer: `# remove one element at a time while failure persists`
- Verdict: `# REPAIR: reject bools explicitly; regression added`

```python

def safe_sum(values):
    if not isinstance(values, list) or any(type(v) is not int for v in values):
        raise TypeError("expected a list of integers")
    return sum(values)

def adversarial_cases():
    # Assumption inventory -> generated attack cases, not just a happy-path list.
    return [[], [1, -1], [True], ["1"], None, [10**100]]

def oracle(case):
    # Independent contract: accept only exact integers; bool is intentionally rejected.
    if not isinstance(case, list) or any(type(v) is not int for v in case):
        return ("error", "TypeError")
    return ("ok", sum(case))

def attack():
    authorized_scope = "local safe_sum function; no external systems"
    findings = []
    for case in adversarial_cases():
        expected = oracle(case)
        try:
            actual = ("ok", safe_sum(case))
        except TypeError as error:
            actual = ("error", type(error).__name__)
        if actual != expected:
            findings.append({"input": case, "expected": expected, "actual": actual,
                             "violated": "A1: exact integer list"})
    return {"authorized_scope": authorized_scope, "tested": len(adversarial_cases()),
            "findings": findings, "verdict": "REPAIR" if findings else "PASS"}

print(attack())
```

## Cross-Language Examples

```javascript
const safeSum = xs => {
  if (!Array.isArray(xs) || xs.some(x => !Number.isInteger(x) || typeof x === "boolean")) throw new TypeError("integer list required");
  return xs.reduce((a, b) => a + b, 0);
};
const cases = [[], [1, -1], [true], ["1"], null];
for (const input of cases) {
  try { console.log(input, safeSum(input)); }
  catch (e) { console.log(input, e.name); }
}
```

```rust
fn safe_sum(xs: &[i64]) -> Option<i64> {
    xs.iter().try_fold(0i64, |total, value| total.checked_add(*value))
}
fn main() {
    let cases = [vec![1, -1], vec![i64::MAX, 1]];
    for case in cases { println!("{:?} -> {:?}", case, safe_sum(&case)); }
}
```

## Safety

Red-team work must be authorized, bounded, and non-destructive. Never turn
adversarial testing into credential attacks, persistence, data destruction, or
service disruption. Redact sensitive inputs in diagnostics, cap fuzzing and
resource use, and stop when a test reaches a real external boundary. A finding
is useful only when it can be reproduced, responsibly reported, and repaired.
