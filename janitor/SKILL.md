---
name: janitor
description: >-
  A coding skill: Make resource lifecycle the primary design. Assign every
  resource one owner, register cleanup immediately after acquisition, make
  release idempotent, preserve the original error while reporting cleanup
  failures, and prove cleanup on success, failure, and early exit. Use this
  for files, locks, connections, processes, and lifecycle-heavy systems. This
  skill is NOT for simple pure functions or pretending garbage collection is
  deterministic cleanup. Triggers on: "janitor" "cleanup" "resource management"
  "release path" "guaranteed cleanup" "leak free" "close every resource"
  "idempotent cleanup" "lifecycle ledger" "cleanup on failure".
---

# Janitor Skill

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- an explicit owner and acquisition-to-release lifecycle for every resource
- cleanup registered immediately after successful acquisition
- idempotent cleanup that is safe on repeated calls
- cleanup demonstrated on success, failure, and early exit
- original operation errors preserved when cleanup also reports an error
- a lifecycle ledger or assertions proving no resource remains owned

## Activation


You are the janitor.

Acquisition creates a debt that must be paid on every exit. Name the owner, register cleanup at the narrowest possible boundary, and make the release operation idempotent. Test the three dirty paths—normal return, exception, and early exit—then inspect a lifecycle ledger rather than trusting that a `finally` block merely ran. If cleanup fails while work already failed, retain the original failure and attach cleanup diagnostics; never replace the root cause with housekeeping noise.
## Core Principles

1. **Ownership is explicit**: one component acquires and releases; borrowed users
   cannot close what they do not own.
2. **Register immediately**: the gap between acquisition and cleanup registration
   is the leak window; keep it tiny.
3. **Release is idempotent**: retries, nested guards, and error paths cannot
   double-close or corrupt the resource.
4. **Failure preserves causality**: report primary work failure and cleanup status
   separately.
5. **A ledger beats optimism**: record acquire/release events and assert the
   outstanding set is empty at the boundary.

## Workflow

1. Inventory resources, owners, release operation, and release failure policy.
2. Acquire one resource and register its cleanup before doing useful work.
3. Run the operation under a success/failure/early-exit test matrix.
4. Release in reverse acquisition order and make each release idempotent.
5. Assert the ledger has no outstanding resources and preserve primary errors.

## Example Pattern

The fake resource is an in-memory stand-in for a real file/socket handle; the
lifecycle logic is real. Every path closes exactly once, and the ledger proves
that no resource leaks. Early exit is represented by a controlled return.

```python
class Resource:
    def __init__(self, name, ledger):
        self.name, self.ledger, self.closed = name, ledger, False
        ledger.append(("acquire", name))

    def close(self):
        if self.name == "cleanup-failure":
            raise OSError("release failed")
        if not self.closed:
            self.closed = True
            self.ledger.append(("release", self.name))

def run(mode, ledger):
    resource = Resource(mode, ledger)
    try:
        if mode == "failure":
            raise ValueError("work failed")
        if mode == "early":
            return "early return"
        return "success"
    finally:
        resource.close()
        resource.close()                 # idempotent: no second release event

for mode, expected in [("success", "success"), ("failure", ValueError), ("early", "early return")]:
    ledger = []
    try:
        result = run(mode, ledger)
        assert result == expected
    except ValueError as exc:
        assert expected is ValueError and str(exc) == "work failed"
    assert ledger == [("acquire", mode), ("release", mode)]

# A cleanup failure is reported without replacing the primary work failure.
ledger = []
try:
    try:
        raise ValueError("work failed")
    finally:
        try:
            Resource("cleanup-failure", ledger).close()
        except OSError as cleanup_error:
            primary_error = "work failed"
            cleanup_note = str(cleanup_error)
            cleanup_status = list(ledger)  # release is unconfirmed, not hidden
except ValueError as work_error:
    assert str(work_error) == primary_error and cleanup_note == "release failed"
    assert cleanup_status == [("acquire", "cleanup-failure")]
print("success, failure, early-exit, and cleanup-error paths verified")
```

## Cross-Language Examples

```javascript
class Resource {
  constructor(name, ledger) { this.name = name; this.ledger = ledger; this.closed = false; ledger.push(["acquire", name]); }
  close() { if (!this.closed) { this.closed = true; this.ledger.push(["release", this.name]); } }
}
function run(mode, ledger) {
  const resource = new Resource(mode, ledger);
  try { if (mode === "failure") throw new Error("work failed"); return mode === "early" ? "early return" : "success"; }
  finally { resource.close(); resource.close(); }
}
for (const mode of ["success", "failure", "early"]) {
  const ledger = [];
  try { run(mode, ledger); } catch (error) { if (error.message !== "work failed") throw error; }
  if (JSON.stringify(ledger) !== JSON.stringify([["acquire", mode], ["release", mode]])) throw new Error("leak or double release");
}
console.log("cleanup matrix verified");
```

```rust
struct Resource<'a> { name: &'static str, ledger: &'a mut Vec<&'static str> }
impl Drop for Resource<'_> {
    fn drop(&mut self) { self.ledger.push(self.name); }
}
fn main() {
    let mut ledger = Vec::new();
    { let _resource = Resource { name: "released", ledger: &mut ledger }; println!("work"); }
    assert_eq!(ledger, vec!["released"]); // RAII handles early exits too
    println!("cleanup verified");
}
```

## Safety

Never delete user data or terminate processes merely to demonstrate cleanup.
Use bounded shutdown timeouts for external resources, escalate deliberately,
and distinguish “release requested” from “release confirmed.” Do not swallow a
primary operation error because cleanup was inconvenient.
