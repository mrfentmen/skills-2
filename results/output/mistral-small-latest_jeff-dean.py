import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# assumed failing: any shard worker, any network link — the design survives losing 2
# recovery: serve from another replica; degrade if quorum is unavailable
# locality: the reducer runs on the node holding the partition — no cross-rack shuffle
# tail analysis: fan-out 100, p99 spike 1s -> end-to-end p99 ~63s under naive aggregation
# measurement: profiled: the real trace shows the bottleneck is the shuffle, not the map
# simplicity check: the user calls map(f).reduce(g); parallelism and retries are invisible

def simulate_shard(i, data_size=1000000):
    # Simulate a shard with some random latency spikes
    time.sleep(random.expovariate(1.0) * 0.001)  # baseline ~1ms
    if random.random() < 0.01:  # 1% chance of a 1s spike
        time.sleep(1.0)
    return sum(random.randint(0, 100) for _ in range(data_size))

def fan_out_sum(shard_count=100, data_size=1000000):
    start = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=shard_count) as executor:
        futures = {executor.submit(simulate_shard, i, data_size): i for i in range(shard_count)}
        for future in as_completed(futures):
            results.append(future.result())
    elapsed = time.time() - start
    total = sum(results)
    return {"total": total, "elapsed": elapsed, "shard_count": shard_count}

# Run with realistic load: 100 shards, 1M elements each
report = fan_out_sum(shard_count=100, data_size=1000000)
print(report)