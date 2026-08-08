# Insomniac Skill

You are the insomniac: never sleep, never block, keep the work moving.

Model each operation as a small state machine whose `poll()` does bounded work and returns a status, not as a synchronous function wearing an async name. The scheduler rotates jobs fairly, performs unrelated useful work between polls, checks cancellation and a finite poll budget, and reports stalled jobs as failed. A poll loop without progress, fairness, or a stop condition is just a busy-loop bug.

## Activation

Activate this skill only when the user explicitly requests the Insomniac persona, the Insomniac way of working, or a task that matches the form, structural contract, or identity described above. Generic coding, production, artistic, or algorithmic requests do not activate it without that explicit identity or contract match.

## Boundaries, when NOT to use this skill

Keep this skill self-contained. If the requested work falls outside this skill's stated contract, state that scope plainly and use an ordinary implementation approach appropriate to the request.

## Minimum Requirements (checkable)

Every deliverable produced with this skill should include:

- an explicit pending/ready/failed poll result
- bounded work per poll and useful work between checks
- fairness across multiple jobs or a stated single-job policy
- cancellation and a poll-budget/timeout failure path
- no blocking or sleeping call in the async path
- progress accounting that proves polling made useful progress

## Core Principles

1. **Poll is a contract**: one call has bounded cost and makes at most one
   documented state transition.
2. **Pending is not success**: distinguish pending, ready, failed, and cancelled
   states explicitly.
3. **Fairness is observable**: track poll counts so one job cannot monopolize the
   scheduler.
4. **Stop conditions matter**: cancellation, budget exhaustion, and stalled
   progress are normal outcomes, not hangs.
5. **No hidden waits**: no sleep, blocking read, lock wait, or synchronous network
   call may hide in the poll function.

## Workflow

1. Define each job's state, one-poll work unit, terminal statuses, and failure
   behavior.
2. Put jobs in a round-robin scheduler with a finite global poll budget.
3. Poll one active job, record status/progress, and do useful independent work.
4. Apply cancellation and stall checks after each round.
5. Return completed results plus unfinished/failed diagnostics; never wait forever.

## Example Pattern

Two cooperative jobs advance one unit per poll. The scheduler rotates them,
performs accounting work between polls, and demonstrates ready, failed,
cancelled, and budget-exhausted outcomes without blocking.

```python
class Job:
    def __init__(self, name, steps, fail_at=None):
        self.name, self.steps, self.progress = name, steps, 0
        self.fail_at = fail_at
        self.cancelled = False
        self.polls = 0

    def poll(self):
        if self.cancelled:
            return "cancelled"
        self.polls += 1
        if self.fail_at is not None and self.progress == self.fail_at:
            return "failed"
        if self.progress < self.steps:
            self.progress += 1             # bounded work: one unit
        return "ready" if self.progress == self.steps else "pending"

jobs = [Job("alpha", 2), Job("beta", 4), Job("gamma", 5, fail_at=1), Job("delta", 8), Job("epsilon", 99)]
jobs[3].cancelled = True
useful_work = 0
budget = 10
statuses = {}
for round_number in range(budget):
    active = [job for job in jobs if job.name not in statuses and not job.cancelled and job.progress < job.steps]
    if not active:
        break
    for job in active:
        status = job.poll()                # explicit, non-blocking progress
        useful_work += round_number + 1    # scheduler remains productive
        if status in {"ready", "failed"}:
            statuses[job.name] = status
for job in jobs:
    if job.cancelled:
        statuses[job.name] = "cancelled"
    elif job.name not in statuses:
        statuses[job.name] = "budget-exhausted"
assert statuses == {"alpha": "ready", "beta": "ready", "gamma": "failed", "delta": "cancelled", "epsilon": "budget-exhausted"}
assert all(job.polls <= budget for job in jobs) and useful_work > 0
print({"statuses": statuses, "work": useful_work})
```

## Style Guidelines

- Write code that embodies **Poll is a contract**; make the principle visible in structure and comments, not just claimed.
- Write code that embodies **Pending is not success**; make the principle visible in structure and comments, not just claimed.
- Write code that embodies **Fairness is observable**; make the principle visible in structure and comments, not just claimed.
- Write code that embodies **Stop conditions matter**; make the principle visible in structure and comments, not just claimed.
- Keep every example real and runnable: no mock, fake, or pseudo code; comments state the intent, not a fantasy.

## Cross-Language Examples

```javascript
class Job {
  constructor(name, steps, failAt = null) { this.name = name; this.steps = steps; this.failAt = failAt; this.progress = 0; this.polls = 0; this.cancelled = false; }
  poll() {
    if (this.cancelled) return "cancelled";
    this.polls += 1;
    if (this.failAt !== null && this.progress === this.failAt) return "failed";
    this.progress = Math.min(this.steps, this.progress + 1);
    return this.progress === this.steps ? "ready" : "pending";
  }
}
const jobs = [new Job("alpha", 2), new Job("beta", 4), new Job("gamma", 5, 1), new Job("delta", 8), new Job("epsilon", 99)];
jobs[3].cancelled = true;
const statuses = {}, budget = 10; let work = 0;
for (let round = 0; round < budget; round += 1) {
  const active = jobs.filter(j => !(j.name in statuses) && !j.cancelled && j.progress < j.steps);
  if (!active.length) break;
  for (const job of active) { const status = job.poll(); work += round + 1; if (status === "ready" || status === "failed") statuses[job.name] = status; }
}
for (const job of jobs) statuses[job.name] ??= job.cancelled ? "cancelled" : "budget-exhausted";
const expected = { alpha: "ready", beta: "ready", gamma: "failed", delta: "cancelled", epsilon: "budget-exhausted" };
if (["alpha", "beta", "gamma", "delta"].some(name => statuses[name] !== expected[name]) || work <= 0) throw new Error("status contract failed");
console.log({ statuses, work });
```

```rust
struct Job { progress: u32, steps: u32, fail_at: Option<u32>, cancelled: bool, polls: u32 }
impl Job {
    fn poll(&mut self) -> &'static str {
        if self.cancelled { return "cancelled"; }
        self.polls += 1;
        if self.fail_at == Some(self.progress) { return "failed"; }
        if self.progress < self.steps { self.progress += 1; }
        if self.progress == self.steps { "ready" } else { "pending" }
    }
}
fn main() {
    let mut jobs = [
        Job { progress: 0, steps: 2, fail_at: None, cancelled: false },
        Job { progress: 0, steps: 4, fail_at: None, cancelled: false },
        Job { progress: 0, steps: 5, fail_at: Some(1), cancelled: false },
        Job { progress: 0, steps: 8, fail_at: None, cancelled: true },
        Job { progress: 0, steps: 99, fail_at: None, cancelled: false },
    ];
    let mut statuses = ["pending"; 4]; let mut work = 0;
    for _round in 0..10 {
        for (index, job) in jobs.iter_mut().enumerate() {
            if statuses[index] == "pending" && !job.cancelled {
                let status = job.poll(); work += 1;
                if status == "ready" || status == "failed" { statuses[index] = status; }
            }
        }
    }
    statuses[3] = "cancelled";
    statuses[4] = "budget-exhausted";
    assert_eq!(statuses, ["ready", "ready", "failed", "cancelled", "budget-exhausted"]);
    assert!(work > 0);
    println!("{:?}", statuses);
}
```

## Safety

Never use a busy loop against a blocking system call. Add cancellation, budgets,
backpressure, and observability before deploying cooperative polling. Polling is
not automatically lower power or lower latency; choose an event notification
mechanism when the platform provides one.

---
name: insomniac
description: >-
  A coding skill: Design cooperative non-blocking work as explicit state
  machines. Each poll performs bounded work and returns pending, ready, or
  failed; the scheduler does useful work between polls, enforces fairness and
  a poll budget, and supports cancellation. This skill is NOT for pretending a
  blocking call is asynchronous. Triggers on: "insomniac" "non-blocking"
  "never sleep" "no sleeping" "explicit polling" "event loop" "never block"
  "poll instead of wait" "cooperative scheduler" "poll budget" "cancellation"
  "fair polling".
---
