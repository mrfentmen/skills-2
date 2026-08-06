---
name: funeral
description: >-
  A coding skill: Treat important values as linear resources. Give each resource
  one owner, consume it through an explicit operation exactly once, invalidate
  the handle immediately, and make use-after-consume fail visibly. Separate
  borrowed inspection from ownership transfer and document cleanup on success
  and failure. Use this for ownership, linear logic, resource handling, and
  memory-safe design. This skill is NOT for ordinary immutable programming or
  pretending that `del` proves secure memory erasure. Triggers on: "funeral"
  "used exactly once" "ownership" "linear logic" "destroy after use" "no alias"
  "transfer of data" "consume once" "use after move" "linear resource".

# Funeral Skill
---

# Funeral Skill

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- a named owner and an explicit consume/transfer operation for each important
  resource
- exactly one successful consumption per resource
- an invalidated handle or compiler-enforced moved value after consumption
- a visible failure for attempted reuse or double cleanup
- separate treatment of borrowed inspection versus ownership transfer
- cleanup behavior documented for both success and failure paths

## Activation


You are the undertaker.

Every linear resource has a life: creation, one owner, optional borrowed inspection, one final consume, and a grave where the handle is invalid. Design APIs so ownership transfer is visible in the call signature or state machine. Never retain an alias “just in case,” never consume twice, and make failure paths close or invalidate the resource too. In languages without compiler-enforced moves, build a checked handle that rejects use after consume rather than pretending ordinary variable deletion is linear logic.
## Core Principles

1. **Ownership is a state machine**: `live -> consumed` is legal; `consumed ->
live` and `consumed -> consumed` are errors.
2. **Borrowing is not copying**: read-only inspection may observe a live resource
   without acquiring ownership, but the borrow cannot outlive or consume it.
3. **One cleanup authority**: exactly one component closes, frees, or commits a
   resource; callers must not guess whether cleanup happened.
4. **Failure still buries**: exceptions and rejected transfers leave no live
   half-owned resource behind.
5. **Make violations loud**: a use-after-consume error is better than silently
   reading stale state.

## Workflow

1. Inventory resources, owners, permitted borrows, and final cleanup action.
2. Define the live/consumed state and the operation that crosses the boundary.
3. Implement the smallest consume-once API and test a double-consume failure.
4. Exercise success and failure paths; assert the handle is invalid afterward.
5. In ownership-safe languages, let the compiler enforce moves; do not recreate
   aliases merely to make the example convenient.

## Style Guidelines

- Mark the owner, borrow, consume, and cleanup boundary in the API or comments.
- Prefer compiler-enforced moves; use checked handles only where the language lacks linear types.
- Make use-after-consume and double-cleanup failures observable in tests.

## Example Pattern

Python does not enforce move semantics, so this example uses a checked handle.
The raw value is private to the handle; `borrow()` is read-only, and `consume()`
invalidates the handle before returning the result. A second consume fails.

```python
class LinearHandle:
    def __init__(self, value):
        self._value = value
        self._live = True

    def borrow(self):
        if not self._live:
            raise RuntimeError("use after consume")
        return self._value              # borrowed inspection, not ownership

    def consume(self):
        if not self._live:
            raise RuntimeError("double consume")
        value, self._value = self._value, None
        self._live = False              # the grave is sealed first
        return value

packet = LinearHandle(bytearray(b"21"))
assert packet.borrow() == bytearray(b"21")
owned = packet.consume()
result = int(owned.decode()) * 2        # final owner uses the resource
owned.clear()                           # cleanup after last use
try:
    packet.consume()
except RuntimeError as exc:
    assert str(exc) == "double consume"
else:
    raise AssertionError("linear resource was consumed twice")
print(result)
```

## Cross-Language Examples

```javascript
class LinearHandle {
  constructor(value) { this.value = value; this.live = true; }
  borrow() { if (!this.live) throw new Error("use after consume"); return this.value; }
  consume() {
    if (!this.live) throw new Error("double consume");
    const value = this.value;
    this.value = undefined;
    this.live = false;
    return value;
  }
}
const packet = new LinearHandle("21");
if (packet.borrow() !== "21") throw new Error("borrow failed");
const owned = packet.consume();
const result = Number(owned) * 2;
try { packet.consume(); throw new Error("double consume accepted"); }
catch (error) { if (error.message === "double consume accepted") throw error; }
console.log(result);
```

```rust
fn consume(packet: Vec<u8>) -> usize {
    let text = String::from_utf8(packet).unwrap(); // ownership moved here
    text.parse::<usize>().unwrap() * 2
}
fn main() {
    let packet = vec![b'2', b'1'];
    let result = consume(packet);
    // `packet` cannot be used here: Rust's move checker rejects a use-after-move.
    assert_eq!(result, 42);
    println!("{}", result);
}
```

## Safety

Linear handling reduces accidental reuse; it does not automatically encrypt or
securely erase bytes. Avoid logging consumed secrets, close external resources
in a guard/finally path, and document whether a failed consume leaves the
resource live or closed. Never silently ignore a double-consume violation.
