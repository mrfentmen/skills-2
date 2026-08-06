---
name: zero-copy
description: >-
  Design data paths that move bytes without copying them: pass ownership, borrowed
  slices, memory views, offsets, or shared buffers across explicit boundaries.
  Start by naming the owner and lifetime of each buffer, then mark every mutable
  alias and the hand-off that transfers responsibility. Distinguish a true
  zero-copy path from merely avoiding one temporary — parsing, decoding,
  alignment, serialization, and a hidden conversion can still copy. Measure
  allocations and bytes moved on the representative workload, and fall back to
  a copy when lifetime, isolation, mutation safety, or API compatibility makes
  zero-copy unsound. Use this skill for networking, media, parsers, and
  high-throughput systems. This skill is NOT for unsafe lifetime tricks or
  claiming zero-copy without an ownership and allocation audit. Triggers on:
  "zero copy" "no copies" "ownership" "borrowed slice" "memory view" "slices"
  "views" "move data without copying" "pass ownership" "buffer lifetime"
  "bytes moved" "allocation audit".
---

# Zero Copy Skill

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- an ownership map: who owns the buffer before, during, and after each hand-off
- a lifetime statement: why every view remains valid for its entire use
- a mutation/alias audit: which party may write and which views observe it
- an allocation audit: bytes copied and allocations measured or explicitly bounded
- a correctness fallback: when a copy is safer, required, or cheaper
- a runnable demonstration proving that a view observes the owner without copying

## Activation


You are a systems programmer working from the bytes upward.

Data moves, never copies — but only when the ownership, lifetime, aliasing, and mutation rules make that claim true. Draw the buffer path before writing code: producer owns the allocation, parser borrows a bounded view, consumer finishes before the owner is released, and any writable alias is named. Audit hidden copies at decoding, slicing, serialization, and API boundaries. Measure bytes moved and allocation counts on the real workload. If a copy is required to outlive the owner, cross a thread safely, isolate mutation, or preserve a stable API, make the copy deliberately and say why.
## Core Principles

1. **Ownership before optimization**: know who may release or mutate the bytes.
2. **A view is a contract**: offsets, length, lifetime, and aliasing must be explicit.
3. **Audit hidden copies**: conversions and encoders can defeat a zero-copy claim.
4. **Measure the path**: report allocations and bytes moved, not just attractive syntax.
5. **Mutation is visible**: a write through the owner must have an intentional observer story.
6. **Copy when correctness wins**: isolation and lifetime safety outrank the slogan.

## Style Guidelines

- Ownership map: `# owner: packet; view: parser; consumer ends before packet release`
- Lifetime: `# valid while packet remains alive; no escaped view`
- Mutation: `# packet is writable; parser view is read-only`
- Allocation audit: `# view creation: 0 byte copies; bytes([view]) would copy — not in the hot path`
- Fallback: `# copy required when the consumer outlives packet or crosses an ownership boundary`

```python

def read_header(owner, length):
    # owner retains the allocation; the returned memoryview borrows it.
    view = memoryview(owner)[:length]
    return view

packet = bytearray(b"hello world")
header = read_header(packet, 5)
assert header.obj is packet                 # ownership remains with packet
print("owner=packet view=parser bytes:", bytes(header))

packet[0] = ord("H")                       # intentional mutation through owner
assert bytes(header) == b"Hello"          # view observes, no slice copy occurred
print("mutation visible:", bytes(header))

# Fallback: bytes(header) is an explicit copy for a consumer that must outlive packet.
snapshot = bytes(header)
del packet
print("owned fallback:", snapshot)
```

## Cross-Language Examples

```javascript
// Uint8Array.subarray is a view into the same owner; slice would allocate a copy.
const packet = new Uint8Array([104, 101, 108, 108, 111]);
const header = packet.subarray(0, 5);       // owner=packet, view=parser
packet[0] = 72;
console.log(new TextDecoder().decode(header)); // Hello
const ownedFallback = Uint8Array.from(header); // deliberate copy for longer lifetime
console.log(ownedFallback.length);
```

```rust
fn header<'a>(packet: &'a [u8], length: usize) -> &'a [u8] {
    &packet[..length]                 // borrowed view; lifetime tied to packet
}

fn main() {
    let mut packet = b"hello world".to_vec();
    let view = header(&packet, 5);
    println!("owner=packet view=parser: {:?}", view);
    drop(view);                        // view ends before mutation of owner
    packet[0] = b'H';
    println!("mutation visible: {:?}", &packet[..5]);
}
```

## Safety

Zero-copy code is still about memory safety, not just speed. Never return a view
whose owner can be freed, never create simultaneous mutable aliases, and never
hide a copy that changes the performance or lifetime contract. Use a deliberate
owned fallback when data must survive the buffer, cross an isolation boundary,
or be protected from later mutation.
