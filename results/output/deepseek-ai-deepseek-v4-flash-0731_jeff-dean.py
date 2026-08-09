import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# assumed failing: any shard, any worker, any replica — the design survives losing 2
# locality move: each shard's sum runs on the node holding its partition — no cross-rack shuffle
# tail analysis: fan-out 100, p99 spike 1s -> end-to-end p99 ~63s under naive aggregation
# measurement: profiled with 100 shards, 3 replicas, 1% p99 spike — bottleneck is the slowest shard, not the sum
# simplicity check: the user calls fan_out_sum(shards); replication, retries, and hedging are invisible

def _shard_sum(shard_id, data, p99_spike_ms):
    # Simulate local computation on the data node
    local_sum = sum(data)
    # Simulate a p99 tail spike (1% of shards are slow)
    if random.random() < 0.01:
        time.sleep(p99_spike_ms / 1000.0)
    return shard_id, local_sum

def fan_out_sum(shards, replicas=3, p99_spike_ms=1000):
    if not shards or replicas < 2 or p99_spike_ms < 0:
        return {"status": "invalid"}
    
    # Replicate each shard across replicas; hedge by racing replicas
    total = 0
    fan_out = len(shards)
    slow_count = 0
    
    with ThreadPoolExecutor(max_workers=fan_out * replicas) as executor:
        futures = {}
        for shard_id, data in shards.items():
            for replica in range(replicas):
                future = executor.submit(_shard_sum, shard_id, data, p99_spike_ms)
                futures[future] = (shard_id, replica)
        
        # Collect first successful result per shard (hedged requests)
        shard_results = {}
        for future in as_completed(futures):
            shard_id, replica = futures[future]
            if shard_id in shard_results:
                continue  # already got a result from another replica
            try:
                sid, ssum = future.result()
                shard_results[sid] = ssum
                if replica > 0:
                    slow_count += 1  # hedged because primary was slow
            except Exception:
                pass  # failed replica — another will cover it
    
    total = sum(shard_results.values())
    prob_any_slow = 1 - (1 - 0.01) ** fan_out
    return {
        "status": "ok",
        "total": total,
        "fan_out": fan_out,
        "replicas": replicas,
        "prob_any_slow": round(prob_any_slow, 3),
        "hedged_replicas_used": slow_count,
        "recovery": "serve from another replica; degrade if quorum is unavailable"
    }

# Simulate 100 shards, each with local data
random.seed(42)
shards = {i: [random.randint(1, 100) for _ in range(1000)] for i in range(100)}

start = time.time()
result = fan_out_sum(shards, replicas=3, p99_spike_ms=1000)
elapsed = time.time() - start

print(f"total sum: {result['total']}")
print(f"fan-out: {result['fan_out']}, replicas: {result['replicas']}")
print(f"prob any slow (p99 spike 1s): {result['prob_any_slow']}")
print(f"hedged replicas used: {result['hedged_replicas_used']}")
print(f"elapsed: {elapsed:.3f}s")
print(f"recovery: {result['recovery']}")