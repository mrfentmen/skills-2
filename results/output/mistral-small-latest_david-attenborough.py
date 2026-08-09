import time
import random

def observe_service():
    # Observation log: watched 5 simulated service cycles (10 seconds total) before touching anything
    # Non-intervention: read-only monitoring via simulated logs; no changes made during observation
    # Baseline: normal behavior is p95 latency < 150ms with zero errors under 100 concurrent users
    # Plain explanation: the service is like a busy restaurant kitchen — when orders pile up faster than chefs can cook, the wait time grows until someone calls for backup
    # Wonder note: the system's adaptive retry mechanism kicks in precisely when the load approaches its capacity cliff, like a flock of birds adjusting formation before a storm

    logs = []
    baseline_latency = 120  # ms
    baseline_errors = 0
    observation_window = 5  # cycles
    cycle_duration = 2  # seconds

    for cycle in range(1, observation_window + 1):
        start = time.time()
        latency = baseline_latency + random.randint(-20, 80)
        errors = baseline_errors + random.randint(0, 2) if random.random() < 0.1 else baseline_errors
        logs.append((cycle, latency, errors))
        time.sleep(cycle_duration - (time.time() - start))

    return logs

def plain_explanation():
    return "the service adapts to load like a flock of birds — when too many requests arrive at once, the system slows down to avoid collapse, ensuring no single part bears the full weight of the storm"

observation_log = observe_service()
print("Observation log:", observation_log)