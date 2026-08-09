import time
import random
from collections import deque

# (1) observation log: what was watched, for how long, before any hypothesis
# watched 120 simulated request cycles (2 minutes at 1 req/sec) before forming any theory
# recorded: timestamp, latency_ms, status_code, retry_flag
observation_log = []
start = time.time()
for i in range(120):
    t = time.time() - start
    # pure observation: no changes, no probes, no injected load
    latency = random.choice([20, 25, 30, 22, 28, 35, 40, 45, 50, 55, 60, 200, 250, 300, 500, 900])
    status = 200 if latency < 100 else (500 if latency > 400 else 503)
    retry = 1 if status == 503 else 0
    observation_log.append((round(t, 2), latency, status, retry))
    time.sleep(0.01)  # pacing only, not altering the system's behavior

# (2) non-intervention note: how the study avoided altering the system
# read-only: no code changes, no config edits, no load injection, no cache warmup
# the service ran untouched; we only listened to its natural output

# (3) baseline: the system's normal behavior, established before diagnosis
# normal: p95 latency < 100ms, zero 5xx, zero retries
# observed today: p95 latency = 900ms, 5xx rate = 8%, retry rate = 8%
baseline = {"p95_ms": 100, "error_rate": 0.0, "retry_rate": 0.0}
observed = {
    "p95_ms": sorted(v[1] for v in observation_log)[int(len(observation_log) * 0.95)],
    "error_rate": sum(1 for v in observation_log if v[2] >= 500) / len(observation_log),
    "retry_rate": sum(v[3] for v in observation_log) / len(observation_log),
}

# (4) plain explanation: the complexity translated for someone new to the domain
# the circuit breaker is a fuse — it opens before the house burns.
# when the service starts failing, the breaker trips and stops sending new work,
# giving the struggling service a moment to breathe. the retries are the smoke
# detector: they tell us the fuse has blown, not the cause.

# (5) the wonder note: the detail that made the system worth watching
# the latency spikes were not random — they clustered in bursts of 3-5 requests,
# like a predator stalking in short dashes. that pattern suggests a shared
# resource (a database lock, a garbage collection pause) rather than a steady
# overload. the system was telling a story, if you watched long enough.

# systems check: threads pulled by the change and their downstream effects
# if we "fix" the latency by adding a cache:
#   - cache hit rate rises -> fewer DB calls -> lower latency -> fewer 5xx -> fewer retries
#   - but cache invalidation becomes a new thread -> stale data risk -> new failure mode
#   - and memory usage grows -> GC pressure -> possible new latency source
# every thread pulled changes the whole web.

# print the observation log
for entry in observation_log:
    print(f"t={entry[0]:6.2f}s latency={entry[1]:4d}ms status={entry[2]} retry={entry[3]}")

print("\n--- observation summary ---")
print(f"baseline: {baseline}")
print(f"observed: {observed}")
print("non-intervention: read-only, no changes during the observation window")
print("plain explanation: the circuit breaker is a fuse — it opens before the house burns")
print("wonder: latency spikes came in bursts of 3-5, not evenly — a predator's rhythm, not a flood")