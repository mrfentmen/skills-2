# Redacted Skill

You are the redaction clerk.

Begin with a data-minimization inventory: what is needed for the answer, what is sensitive, and what must never enter logs, metrics, exceptions, caches, or the return value. Process one record at a time, derive only the required aggregate, then clear mutable sensitive fields at the last-use boundary. Return a small result plus an honest retention report; do not claim that language-level deletion securely wipes memory. If a field is not needed, refuse to retain it rather than copying it "for later."

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- a field inventory separating required output, transient sensitive data, and
  forbidden retention
- computation of the result without logging or returning raw sensitive values
- immediate clearing or removal of mutable sensitive fields after their last use
- an output containing only the required aggregate/result
- a retention report that documents fields refused and the cleanup boundary
- an explicit caveat about the runtime's memory-erasure guarantees

## Core Principles

1. **Purpose before collection**: define the output schema before touching input
   fields; collection without purpose is a retention bug.
2. **Minimize at the boundary**: sanitize as soon as a record crosses into the
   component, not after raw values have spread through helpers and logs.
3. **Last use is explicit**: name the line after which each sensitive field is
   cleared, and never include it in diagnostics.
4. **Aggregates over records**: retain counts, categories, or tokens needed for
   the answer—not the raw subjects that produced them.
5. **Honest erasure claims**: clearing a mutable container limits application
   retention but does not promise secure physical memory wiping.

## Workflow

1. Write a retention table: field, purpose, sensitivity, last use, cleanup.
2. Reject or quarantine fields that are not required for the requested result.
3. Process records in bounded scope and compute only the approved aggregate.
4. Clear mutable sensitive fields immediately after their final use.
5. Assert that the returned object contains no raw secret and emit only the
   retention metadata needed for audit.
6. Test that input containers no longer retain forbidden fields while stating
   what the test cannot prove about allocator memory.

## Example Pattern

The report needs only the number of active records and the number of records
that carried a token. It does not need an email address or token value. Each
mutable record is reduced in place immediately after classification.

```python
def summarize_and_redact(records):
    # Retention table:
    # active -> aggregate; token -> count only, then clear; email -> never keep.
    active_count = 0
    token_records = 0
    for record in records:
        active = bool(record.get("active"))
        had_token = bool(record.get("token"))
        active_count += active
        token_records += had_token
        record.clear()                 # last use of all raw fields
        record.update({"redacted": True})

    result = {
        "active_count": active_count,
        "token_records": token_records,
        "refused_to_retain": ["email", "token", "raw_record"],
        "cleanup_boundary": "after per-record classification",
        "erasure_limit": "container cleared; secure memory wiping not guaranteed",
    }
    assert all("token" not in record and "email" not in record for record in records)
    return result

records = [
    {"email": "a@example.test", "token": "secret-a", "active": True},
    {"email": "b@example.test", "token": "", "active": False},
]
report = summarize_and_redact(records)
assert report["active_count"] == 1
assert report["token_records"] == 1
assert records == [{"redacted": True}, {"redacted": True}]
assert "secret-a" not in repr(report)
print(report)
```

## Cross-Language Examples

```javascript
function summarizeAndRedact(records) {
  let activeCount = 0;
  let tokenRecords = 0;
  for (const record of records) {
    activeCount += record.active ? 1 : 0;
    tokenRecords += record.token ? 1 : 0;
    delete record.email;              // last use boundary
    delete record.token;
    delete record.active;
    record.redacted = true;
  }
  return {
    activeCount,
    tokenRecords,
    refusedToRetain: ["email", "token", "raw_record"],
    erasureLimit: "object fields deleted; secure memory wiping not guaranteed",
  };
}
const records = [
  { email: "a@example.test", token: "secret-a", active: true },
  { email: "b@example.test", token: "", active: false },
];
const report = summarizeAndRedact(records);
if (report.activeCount !== 1 || report.tokenRecords !== 1 || records[0].token !== undefined) {
  throw new Error("redaction contract failed");
}
console.log(report);
```

```rust
struct Record { email: String, token: String, active: bool }

fn summarize_and_redact(records: &mut [Record]) -> (usize, usize) {
    let mut active = 0;
    let mut token_records = 0;
    for record in records {
        active += record.active as usize;
        token_records += (!record.token.is_empty()) as usize;
        record.email.clear();            // mutable buffers are emptied at last use
        record.token.clear();
        record.active = false;
    }
    (active, token_records)
}

fn main() {
    let mut records = vec![
        Record { email: "a@example.test".into(), token: "secret-a".into(), active: true },
        Record { email: "b@example.test".into(), token: String::new(), active: false },
    ];
    let report = summarize_and_redact(&mut records);
    assert_eq!(report, (1, 1));
    assert!(records.iter().all(|r| r.email.is_empty() && r.token.is_empty()));
    println!("active={}, token_records={}", report.0, report.1);
}
```

## Safety

Minimization is not encryption, access control, or guaranteed secure deletion.
Do not print secrets in examples, logs, error messages, snapshots, or tests.
For high-sensitivity material use an appropriate secret store, cryptographic
erasure strategy, and platform-specific memory controls; document residual
risk instead of overstating what the language runtime can guarantee.

---
name: redacted
description: >-
  A coding skill: Compute the required result while minimizing exposure at
  every boundary. Classify fields before processing, keep only the smallest
  aggregate needed, clear mutable sensitive fields immediately after use, and
  return a retention report that names what was refused. State the limits of
  runtime erasure: ordinary deletion is not guaranteed secure memory wiping.
  Use this for privacy-preserving computation, secret handling, and data
  minimization. This skill is NOT for hiding unsafe behavior or claiming that
  `del` proves a secret is gone. Triggers on: "redacted" "privacy"
  "minimize exposure" "sensitive values" "data minimization" "refuse to retain"
  "secret handling" "field-level minimization" "retention report" "erase".
---
