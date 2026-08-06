---
name: blind
description: >-
  A coding skill: Treat the input as genuinely opaque and expose it only
  through a fixed capability set of approved questions. The solver must not
  inspect, copy, stringify, hash, index, serialize, or retain the value;
  its result is a function of question answers alone. Use this for privacy
  boundaries, oracle algorithms, and capability-based computation. This skill
  is NOT for ordinary parsing or a wrapper that secretly forwards the value.
  Triggers on: "blind" "opaque input" "fixed questions" "question only"
  "predicate" "blind oracle" "capability boundary" "no inspection"
  "fixed set of questions" "fail closed".
---

# Blind Skill

You are blind by design: the value is behind a capability boundary and may be queried only through a fixed, documented question set.

Separate the oracle adapter from the solver so the solver cannot accidentally receive the value. Record question names and answers, reject every question outside the allowlist, and return "undetermined" rather than guessing when the answers do not support a conclusion. Prove non-interference by showing that two hidden values with the same answer transcript produce the same result.

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- a named, closed set of questions that may touch the opaque input
- a solver that receives only question names and primitive answers
- no inspection, copy, stringify, hash, index, serialization, or retained alias
  of the underlying value
- explicit handling for unknown questions and malformed answers
- a result that can be reconstructed from the answer transcript alone
- a fail-closed behavior when the available questions cannot determine the
  requested result

## Core Principles

1. **Question names are capabilities**: an allowlist, not an arbitrary callback,
   defines what information may cross the boundary.
2. **Primitive answers only**: booleans, bounded enums, or documented numbers
   cross the boundary; no object or reference escapes.
3. **Transcript determinism**: the solver must be a pure function of the
   approved answers and question order.
4. **Fail closed**: unknown questions, malformed answers, and insufficient
   information become explicit errors or an undetermined result.
5. **Blindness is testable**: test the solver with two different hidden objects
   that produce the same answers and confirm identical output.

## Workflow

1. Write the question allowlist and answer schema before implementing logic.
2. Build a narrow adapter that validates names and converts answers to primitive
   values; never return the hidden object.
3. Run the solver against that adapter while recording a transcript.
4. Check the transcript for completeness and contradictions.
5. Return a classification only when the fixed questions determine it; otherwise
   return a structured `undetermined` result.
6. Test non-interference with distinct hidden values sharing the same transcript.

## Example Pattern

The solver classifies an opaque account using exactly three approved questions.
It never receives the account object, and its non-interference test uses two
accounts that answer identically.

```python
QUESTIONS = ("is_active", "has_admin_role", "quota_at_least_10")

def classify(ask):
    transcript = []
    answers = {}
    for name in QUESTIONS:
        answer = ask(name)
        if not isinstance(answer, bool):
            raise ValueError(f"malformed answer for {name}")
        transcript.append((name, answer))
        answers[name] = answer

    if answers["has_admin_role"] and answers["is_active"]:
        label = "active-admin"
    elif answers["is_active"] and answers["quota_at_least_10"]:
        label = "active-capable"
    else:
        label = "ordinary-or-inactive"
    return {"label": label, "transcript": tuple(transcript)}

def adapter(account):
    # Only this adapter sees the hidden object; the solver gets bools only.
    def ask(name):
        if name not in QUESTIONS:
            raise KeyError("question not permitted")
        if name == "is_active":
            return account["active"]
        if name == "has_admin_role":
            return "admin" in account["roles"]
        return account["quota"] >= 10
    return ask

first = classify(adapter({"active": True, "roles": ["admin"], "quota": 2}))
second = classify(adapter({"active": True, "roles": ["admin"], "quota": 2}))
# Distinct hidden objects with the same answers produce the same transcript.
assert first["transcript"] == second["transcript"]
assert first["label"] == second["label"] == "active-admin"
print(first["label"], len(first["transcript"]))
```

## Cross-Language Examples

```javascript
const QUESTIONS = ["is_active", "has_admin_role", "quota_at_least_10"];

function classify(ask) {
  const answers = new Map();
  for (const name of QUESTIONS) {
    const answer = ask(name);
    if (typeof answer !== "boolean") throw new Error(`bad answer: ${name}`);
    answers.set(name, answer);
  }
  const label = answers.get("has_admin_role") && answers.get("is_active")
    ? "active-admin"
    : answers.get("is_active") && answers.get("quota_at_least_10")
      ? "active-capable" : "ordinary-or-inactive";
  return { label, answerCount: answers.size };
}
function adapter(account) {
  return name => {
    if (!QUESTIONS.includes(name)) throw new Error("question not permitted");
    if (name === "is_active") return account.active;
    if (name === "has_admin_role") return account.roles.includes("admin");
    return account.quota >= 10;
  };
}
const a = classify(adapter({ active: true, roles: ["admin"], quota: 2 }));
const b = classify(adapter({ active: true, roles: ["admin"], quota: 99 }));
if (a.label !== b.label || a.label !== "active-admin") throw new Error("non-interference failed");
console.log(a);
```

```rust
const QUESTIONS: [&str; 3] = ["is_active", "has_admin_role", "quota_at_least_10"];

fn classify<F>(mut ask: F) -> &'static str
where F: FnMut(&str) -> bool {
    let mut active = false;
    let mut admin = false;
    let mut capable = false;
    for question in QUESTIONS {
        match question {
            "is_active" => active = ask(question),
            "has_admin_role" => admin = ask(question),
            "quota_at_least_10" => capable = ask(question),
            _ => unreachable!(),
        }
    }
    if active && admin { "active-admin" }
    else if active && capable { "active-capable" }
    else { "ordinary-or-inactive" }
}

fn main() {
    let label = classify(|question| match question {
        "is_active" => true,
        "has_admin_role" => true,
        "quota_at_least_10" => false,
        _ => false,
    });
    assert_eq!(label, "active-admin");
    println!("{}", label);
}
```

## Safety

No mock, fake, or pseudo code — the examples perform real classification. A
blind interface is not a security guarantee by itself: document who owns the
adapter, validate every question and answer, and avoid claiming confidentiality
that the runtime cannot provide. Never use blindness to conceal unsafe access.
