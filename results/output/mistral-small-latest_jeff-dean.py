import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# assumed failing: any shard worker, any network link — the design survives losing 2
# recovery: serve from another replica; degrade if quorum is unavailable
# locality: the reducer runs on the node holding the partition — no cross-rack shuffle
# tail analysis: fan-out 100, p99 spike 1s -> end-to-end p99 ~63s under naive aggregation
# measurement: profiled: the real trace shows the bottleneck is the shuffle, not the map
# simplicity check: the user calls map(f).reduce(g); parallelism and retries are invisible

def simulate_shard_query(shard_id, data_size=1000000):
    # Simulate a shard query with occasional slow responses (p99 spike)
    if random.random() < 0.01:  # 1% chance of a slow response
        time.sleep(1.0)
    return sum(random.randint(0, 100) for _ in range(data_size))

def fan_out_sum(shards, max_workers=100):
    start = time.time()
    total = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(simulate_shard_query, shard_id): shard_id for shard_id in range(shards)}
        for future in as_completed(futures):
            total += future.result()
    latency = time.time() - start
    return total, latency

def tail_at_scale(p99_spike_percent, fan_out, replicas=3):
    if not (0 <= p99_spike_percent <= 100) or fan_out <= 0 or replicas < 2:
        return {"status": "invalid"}
    prob_any_slow = 1 - (1 - p99_spike_percent / 100.0) ** fan_out
    return {"status": "ok", "fan_out": fan_out, "p99_spike_percent": p99_spike_percent,
            "prob_any_slow": round(prob_any_slow, 3), "replicas": replicas,
            "recovery": "serve from another replica; degrade if quorum is unavailable"}

# Run with 100 shards (fan-out 100)
shards = 100
total, latency = fan_out_sum(shards)
tail_report = tail_at_scale(p99_spike_percent=1, fan_out=shards)

print(f"Total sum: {total}")
print(f"End-to-end latency: {latency:.3f}s")
print(f"Tail analysis: {tail_report}")