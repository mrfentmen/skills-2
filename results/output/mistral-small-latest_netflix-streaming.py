def choose_bitrate(buffer_secs, ladder, low=5, high=15):
    # buffer-based ABR rule: step up when buffer > 15s, step down when buffer < 5s
    # the buffer is the shock absorber; decisions are client-side, not server-side
    for rate in sorted(ladder, reverse=True):
        if buffer_secs >= high:
            return rate          # deep buffer: step up
        if buffer_secs < low:
            return ladder[0]     # shallow buffer: step down BEFORE the stall
    return ladder[len(ladder) // 2]

def qoe(startup_ms, rebuffer_ratio, avg_bitrate):
    # QoE metric set: startup time, rebuffering ratio, delivered quality
    return {"startup_ms": startup_ms, "rebuffer_ratio": rebuffer_ratio,
            "quality_ok": avg_bitrate >= 2_000_000}

def chaos_monkey(instances, killed):
    # chaos story: every deploy kills 1 instance; survivors must serve
    survivors = instances - killed
    return {"instances": instances, "killed": killed, "survivors": survivors,
            "resilient": survivors > 0}

def load_shed(telemetry_bps, recs_bps, video_bps):
    # load-shedding order: shed background telemetry -> recs -> THEN the video core
    if telemetry_bps > 1_000_000:
        return "shed telemetry"
    if recs_bps > 5_000_000:
        return "shed recs"
    if video_bps > 10_000_000:
        return "shed video"
    return "all_ok"

def ab_test_policy(policy_a, policy_b, buffer_secs, ladder):
    # experiment plan: A/B test ABR policy with Bayesian rigor over 48h
    result_a = choose_bitrate(buffer_secs, ladder) if policy_a else ladder[0]
    result_b = choose_bitrate(buffer_secs, ladder) if policy_b else ladder[0]
    return {"policy_a": result_a, "policy_b": result_b}

ladder = [300_000, 800_000, 1_500_000, 3_000_000, 6_000_000]

# Demo outputs
print("ABR selection:", choose_bitrate(20, ladder))   # 6_000_000 — deep buffer, step up
print("ABR selection:", choose_bitrate(3, ladder))    # 300_000 — step down before a stall
print("QoE metrics:", qoe(900, 0.0, 3_000_000))
print("Chaos outcome:", chaos_monkey(5, 1))
print("Load shed:", load_shed(2_000_000, 3_000_000, 12_000_000))
print("A/B test:", ab_test_policy(True, False, 10, ladder))