# Quiescent Skill

You are the conductor of a live system.

Before touching shared state, close the gates to new work, drain callbacks until no observer is running or queued, and make the replacement in one critical section. Validate every invariant while the system is still quiet; reopen activity only after validation succeeds, and release deferred work through the normal queue rather than running it inside the commit. If validation fails, preserve the old state and remain closed or roll back explicitly. A lock is only one part of quiescence, never the whole claim.

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- a phase flag that rejects or defers new work while quiescing
- a drain loop that reaches a defined quiet point (`queued == 0` and
  `running == 0`, or an equivalent barrier)
- an atomic state transition in a lock/critical section
- invariant validation before activity resumes
- deferred work released only after a successful commit
- failure behavior that leaves the old state or a safely closed system intact

## Core Principles

1. **Close, drain, commit, reopen**: make the lifecycle visible instead of
   relying on an incidental lock.
2. **Drain to a fixed point**: callbacks may enqueue more callbacks; quiescence
   is reached only when both the queue and running count are empty.
3. **Atomic means all-or-nothing**: prepare a candidate off to the side, then
   publish it under the lock only after invariants pass.
4. **Observers see epochs, not half-state**: publish one complete version and
   make the version transition explicit.
5. **Recovery is part of the protocol**: a failed validation never exposes the
   candidate and never silently resumes normal traffic.

## Workflow

1. Define what counts as work, what may enqueue work, and which invariants the
   state must satisfy.
2. Set `accepting = false` so new events are deferred, then drain existing work
   until the queue and active callback count are both zero.
3. Prepare the candidate without publishing it.
4. Under the state lock, re-check the quiet point, validate the candidate, and
   publish it atomically.
5. Reopen only after the new state is valid; move deferred work to the queue and
   dispatch it through the ordinary path.
6. On error, retain the old state and report that the system stayed closed.

## Example Pattern

This deterministic event store demonstrates all phases. An observer that emits
while the store is quiet is deferred, not lost or allowed to mutate the state
mid-commit.

```python
from collections import deque
from threading import Condition, RLock

class QuiescentStore:
    def __init__(self):
        self.state = {"version": 0, "items": []}
        self.queue = deque()
        self.deferred = deque()
        self.accepting = True
        self.running = 0
        self.lock = RLock()
        self.changed = Condition(self.lock)

    def emit(self, callback):
        with self.changed:
            (self.queue if self.accepting else self.deferred).append(callback)
            self.changed.notify_all()

    def drain(self):
        while True:
            with self.changed:
                while not self.queue and self.running:
                    self.changed.wait()  # let active callbacks report completion
                if not self.queue and self.running == 0:
                    return
                callback = self.queue.popleft()
                self.running += 1
            try:
                callback()
            finally:
                with self.changed:
                    self.running -= 1
                    self.changed.notify_all()

    def transition(self, items):
        with self.changed:
            self.accepting = False       # close the gate first
        self.drain()                      # reach queue/running == 0
        candidate = {"version": self.state["version"] + 1, "items": list(items)}
        if len(candidate["items"]) != len(set(candidate["items"])):
            raise ValueError("duplicate items: old state remains published")
        with self.changed:                # atomic publish while quiet
            assert not self.queue and self.running == 0
            assert candidate["version"] == self.state["version"] + 1
            self.state = candidate
            self.accepting = True         # reopen only after invariants hold
            self.queue.extend(self.deferred)
            self.deferred.clear()
            self.changed.notify_all()

    def run_ready(self):
        self.drain()

store = QuiescentStore()
store.emit(lambda: store.emit(lambda: None))  # callback creates deferred work
store.transition(["alpha", "beta"])
store.run_ready()
assert store.state == {"version": 1, "items": ["alpha", "beta"]}
assert not store.deferred and not store.queue
print(store.state)
```

## Cross-Language Examples

```javascript
class QuiescentStore {
  constructor() {
    this.state = { version: 0, items: [] };
    this.queue = [];
    this.deferred = [];
    this.accepting = true;
  }
  emit(callback) { (this.accepting ? this.queue : this.deferred).push(callback); }
  drain() {
    while (this.queue.length) this.queue.shift()();
  }
  transition(items) {
    this.accepting = false;
    this.drain();
    const unique = new Set(items);
    if (unique.size !== items.length) throw new Error("duplicate items");
    const candidate = { version: this.state.version + 1, items: [...items] };
    this.state = candidate;             // one synchronous publication
    this.accepting = true;
    this.queue.push(...this.deferred);
    this.deferred = [];
    this.drain();
  }
}
const store = new QuiescentStore();
store.emit(() => store.emit(() => {}));
store.transition(["alpha", "beta"]);
if (store.state.version !== 1 || store.queue.length || store.deferred.length) throw new Error("not quiet");
console.log(store.state);
```

```rust
struct Store {
    version: u64,
    items: Vec<&'static str>,
    accepting: bool,
    queue: Vec<fn(&mut Store)>,
    deferred: Vec<fn(&mut Store)>,
}

impl Store {
    fn emit(&mut self, callback: fn(&mut Store)) {
        if self.accepting { self.queue.push(callback); }
        else { self.deferred.push(callback); }
    }
    fn drain(&mut self) {
        while let Some(callback) = self.queue.pop() { callback(self); }
    }
    fn transition(&mut self, items: Vec<&'static str>) {
        self.accepting = false;             // close admission
        self.drain();                       // queue/running barrier in this synchronous model
        // Exclusive `&mut Store` access is this example's critical section;
        // it is synchronous and not a substitute for a thread-safe lock.
        assert!(items.windows(2).all(|w| w[0] != w[1]));
        let candidate = (self.version + 1, items);
        self.version = candidate.0;         // atomic publication: no callback runs here
        self.items = candidate.1;
        self.accepting = true;              // reopen only after validation
        self.queue.append(&mut self.deferred);
    }
}

fn enqueue_follow_up(store: &mut Store) { store.emit(|_| {}); }

fn main() {
    let mut store = Store { version: 0, items: vec!["old"], accepting: true,
        queue: vec![], deferred: vec![] };
    store.emit(enqueue_follow_up);
    store.transition(vec!["gamma"]);
    store.drain();
    assert_eq!(store.version, 1);
    assert_eq!(store.items, vec!["gamma"]);
    assert!(store.queue.is_empty() && store.deferred.is_empty());
    println!("version={}", store.version);
}
```

## Safety

Do not claim quiescence in a system whose callbacks can run outside the
controlled queue, whose interrupts cannot be masked, or whose workers lack a
join/barrier protocol. Use timeouts and an explicit failure state in production;
never force-release a lock or discard events silently. The examples avoid
external processes and perform only in-memory transitions.

---
name: quiescent
description: >-
  A coding skill: Change shared state only through a quiescence protocol.
  Stop new observers, drain already-queued work to a fixed point, commit the
  replacement under an atomic critical section, verify invariants, and reopen
  activity only after the commit is valid. Use this for event systems, hot
  reloads, UI stores, and concurrent services. This skill is NOT for putting
  a mutex around every function or pretending a lock alone drains callbacks.
  Triggers on: "quiescent" "quiet point" "quiescence protocol" "drain
  callbacks" "atomic transition" "deferred events" "hot reload" "no
  observers" "invariant before resume".
---
