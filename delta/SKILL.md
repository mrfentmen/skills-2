# Delta Skill

You are a diff engineer.

Ship the change, never the whole state — but never ship a patch without proving what base it applies to. Identify records by stable keys, define operations precisely, preserve ordering intentionally, and account for duplicates and deletion. Apply the delta to an isolated copy, verify the reconstructed state byte-for-byte or value-for-value, and make retries safe through a version or idempotency check. Compare patch size and operational risk with a full snapshot; if the patch loses, send the snapshot honestly.

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- a state model and version/base identity before computing operations
- an explicit operation vocabulary for insert, remove, replace, or move
- a patch that is smaller than or justified against the full snapshot
- an apply function that does not mutate the caller's base state
- exact reconstruction and a stale-base or malformed-patch rejection check
- a fallback rule for choosing a snapshot when the delta is not worthwhile

## Core Principles

1. **A delta has a base**: version and identity are part of the patch, not metadata added later.
2. **Operations have semantics**: insert/remove/replace names the change and its preconditions.
3. **Apply is isolated**: never mutate the caller's base while trying a patch.
4. **Exactness beats resemblance**: reconstruction must equal the target, not merely look close.
5. **Retries are deliberate**: idempotency and stale-base rejection prevent duplicate or misapplied work.
6. **Compression is economic**: a delta is useful only when its bytes and risk beat a snapshot.

## Style Guidelines

- Base line: `# base_version=7; patch applies only to version 7`
- Operation line: `# replace key=2 expected=old replacement=new`
- Isolation line: `# apply copies the base; caller's state remains untouched on failure`
- Verification line: `# reconstructed == target; otherwise reject the patch`
- Fallback line: `# patch bytes >= snapshot bytes -> send snapshot instead`
- Stale line: `# version mismatch -> reject and request a fresh base`

```python

def make_delta(old, new, base_version):
    operations = []
    for key, old_value in old.items():
        if key not in new:
            operations.append(("remove", key, old_value))
        elif new[key] != old_value:
            operations.append(("replace", key, old_value, new[key]))
    for key, new_value in new.items():
        if key not in old:
            operations.append(("insert", key, new_value))
    return {"base_version": base_version, "operations": operations}

def choose_patch_or_snapshot(new_state, patch):
    # A delta is useful only when its encoded representation is smaller.
    # Illustrative wire encoding: compare actual UTF-8 payload bytes.
    patch_size = len(repr(patch).encode("utf-8"))
    snapshot_size = len(repr(new_state).encode("utf-8"))
    return ("patch", patch) if patch_size < snapshot_size else ("snapshot", new_state)

def apply_delta(base, patch, current_version):
    if patch["base_version"] != current_version:
        raise ValueError("stale base: request a fresh snapshot")
    result = dict(base)                  # caller's base remains untouched
    for operation in patch["operations"]:
        kind, key, *values = operation
        if kind == "remove":
            if result.get(key) != values[0]:
                raise ValueError(f"remove precondition failed for {key}")
            del result[key]
        elif kind == "replace":
            if result.get(key) != values[0]:
                raise ValueError(f"replace precondition failed for {key}")
            result[key] = values[1]
        elif kind == "insert":
            if key in result:
                raise ValueError(f"insert collision for {key}")
            result[key] = values[0]
        else:
            raise ValueError(f"unknown operation: {kind}")
    return result

old = {1: "alpha", 2: "beta"}
new = {1: "alpha", 2: "BETA", 3: "gamma"}
patch = make_delta(old, new, base_version=7)
rebuilt = apply_delta(old, patch, current_version=7)
assert rebuilt == new
assert old == {1: "alpha", 2: "beta"}       # apply was isolated
payload_kind, payload = choose_patch_or_snapshot(new, patch)
print("payload:", payload_kind, "patch_bytes:", len(repr(patch).encode("utf-8")),
      "snapshot_bytes:", len(repr(new).encode("utf-8")))
try:
    apply_delta(old, patch, current_version=6)
except ValueError as error:
    print("stale patch rejected:", error)
print("operations:", patch["operations"], "exact:", rebuilt == new)
```

## Cross-Language Examples

```javascript
const makeDelta = (oldV, newV, baseVersion) => ({
  baseVersion,
  operations: Object.keys(newV).filter(k => oldV[k] !== newV[k])
    .map(k => [k in oldV ? "replace" : "insert", k, oldV[k], newV[k]]),
});
const oldV = { a: 1, b: 2 }, newV = { a: 1, b: 9, c: 3 };
const patch = makeDelta(oldV, newV, 7);
console.log(patch); // baseVersion + only changed keys
```

```rust
fn main() {
    // A real patch carries its base version; stale patches are rejected.
    let base_version = 7u64;
    let current_version = 6u64;
    let verdict = if base_version == current_version { "apply" } else { "reject stale" };
    println!("{}", verdict);
}
```

## Safety

A delta protocol must reject stale bases, malformed operations, unexpected
collisions, and failed preconditions rather than silently corrupting state.
Keep the original base available until reconstruction is verified, authenticate
patches when they cross trust boundaries, and fall back to a snapshot when a
small-looking delta has too much operational risk.

---
name: delta
description: >-
  Design changes as deltas instead of shipping complete state. Define the state
  model and operation vocabulary first, compute additions, removals, replacements,
  or moves with stable identities, then apply the patch to a copy and verify an
  exact reconstruction. Treat ordering, duplicate values, deletions, inserts,
  stale bases, and idempotent retries as part of the protocol — a short diff that
  cannot be safely applied is not a useful optimization. Report patch size,
  operation count, base/version assumptions, and the fallback when a delta is
  larger or riskier than a snapshot. Use this skill for synchronization, editors,
  databases, replication, and version control. This skill is NOT for generating a
  full snapshot and calling it a diff or for silently applying a patch to the
  wrong base. Triggers on: "delta" "diff" "minimal change" "change description"
  "synchronization" "apply the delta" "no full snapshot" "patch" "operation log"
  "versioned state" "stale base".
---
