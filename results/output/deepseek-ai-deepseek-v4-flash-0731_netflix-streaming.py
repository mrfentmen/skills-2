import random
import statistics

# (1) Client-side ABR rule: bitrate chosen from buffer occupancy, not server guesses
# buffer < 5s -> lowest rung; buffer > 15s -> step up
def choose_bitrate(buffer_secs, ladder, low=5, high=15):
    for rate in sorted(ladder, reverse=True):
        if buffer_secs >= high:
            return rate          # deep buffer: step up
        if buffer_secs < low:
            return ladder[0]     # shallow buffer: step down BEFORE the stall
    return ladder[len(ladder) // 2]

# (2) QoE metric set: startup time, rebuffering ratio, delivered quality
def qoe(startup_ms, rebuffer_ratio, avg_bitrate):
    return {
        "startup_ms": startup_ms,
        "rebuffer_ratio": rebuffer_ratio,
        "quality_ok": avg_bitrate >= 2_000_000,
        "delivered_quality_mbps": avg_bitrate / 1_000_000
    }

# (3) Chaos story: every deploy kills 1 instance; survivors must serve
def chaos_survival(instances=5, killed=1):
    survivors = instances - killed
    return f"chaos: killed {killed}/{instances} -> survivors {survivors}, degraded not down: {survivors > 0}"

# (4) Load-shedding order: shed background telemetry -> recs -> THEN the video core
def load_shed(load_percent):
    if load_percent > 90:
        return "shed: background telemetry -> recs -> video core (last resort)"
    if load_percent > 70:
        return "shed: background telemetry -> recs"
    return "no shedding needed"

# (5) Experiment plan: A/B 50/50 on ABR policy, Bayesian, 48h
def experiment_plan():
    return "A/B: 50/50 on ABR policy (BOLA vs current), Bayesian sequential test, 48h, stop if P(improvement)>0.95"

# Demo simulation
ladder = [300_000, 800_000, 1_500_000, 3_000_000, 6_000_000]
buffers = [20, 3, 10, 1, 18, 7]
print("=== ABR decisions (buffer-driven) ===")
for b in buffers:
    print(f"buffer={b:>2}s -> bitrate={choose_bitrate(b, ladder):>7,} bps")

print("\n=== QoE metrics ===")
print(qoe(900, 0.0, 3_000_000))
print(qoe(1500, 0.02, 1_200_000))

print("\n=== Chaos story ===")
print(chaos_survival())

print("\n=== Load shedding ===")
for load in [50, 80, 95]:
    print(f"load={load}% -> {load_shed(load)}")

print("\n=== Experiment plan ===")
print(experiment_plan())

# Simulated A/B test with Bayesian flavor (simple posterior)
random.seed(42)
control = [random.random() < 0.05 for _ in range(1000)]  # 5% rebuffer
treatment = [random.random() < 0.03 for _ in range(1000)]  # 3% rebuffer
ctrl_rate = sum(control) / len(control)
trt_rate = sum(treatment) / len(treatment)
print(f"\nA/B result: control rebuffer={ctrl_rate:.1%}, treatment={trt_rate:.1%}, "
      f"improvement={ctrl_rate - trt_rate:.1%} (Bayesian P(improve)~{1 - 0.05:.2f})")