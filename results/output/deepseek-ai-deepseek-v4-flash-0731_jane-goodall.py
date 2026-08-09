import random
from datetime import datetime, timedelta

# (1) Observation plan:
# Watch the "checkout-svc" event stream for 14 days in production traffic
# (not 10 minutes in staging). Record every event's timestamp, latency_ms,
# and error flag. Conditions: normal weekday load plus one planned deploy
# on day 7 to see if behavior changes.

# (2) Named individuals:
# "checkout-svc" — a payment service with a history: since the April 12 deploy,
# its error rate has been creeping upward every Tuesday. Today is day 1 of
# observation; it has 3 known past incidents, all on Tuesdays.

# (3) Challenged assumption:
# Everyone assumes the database is the bottleneck. The logs say otherwise —
# we will test whether latency spikes correlate with error bursts, not DB load.

# (4) Evidence trail:
# Each observation is a dict with timestamp (ISO), context (day number, deploy flag),
# latency_ms, and error (bool). No vibes, only numbers.

# (5) Patient-action note:
# Add one page of monitoring per week (e.g., a new dashboard panel for error
# correlation). In a quarter, the system becomes visible; in a year, we can
# predict Tuesdays before they happen.

random.seed(42)
start = datetime(2026, 8, 1, 9, 0, 0)
events = []
for i in range(14 * 24 * 60):  # one event per minute for 14 days
    ts = start + timedelta(minutes=i)
    day = (ts - start).days + 1
    is_tuesday = ts.weekday() == 1
    deploy_day = (day == 7)
    # baseline latency 100ms, Tuesday adds 20ms, deploy day adds 50ms
    latency = 100 + (20 if is_tuesday else 0) + (50 if deploy_day else 0)
    latency += random.gauss(0, 15)
    # error rate: 1% baseline, 5% on Tuesday, 10% on deploy day
    err_prob = 0.01 + (0.04 if is_tuesday else 0) + (0.05 if deploy_day else 0)
    error = random.random() < err_prob
    events.append({
        "timestamp": ts.isoformat(),
        "day": day,
        "deploy": deploy_day,
        "latency_ms": round(max(0, latency), 1),
        "error": error,
    })

# Focal follow: sustained observation over the full window
def focal_follow(events, min_day):
    window = [e for e in events if e["day"] >= min_day]
    if not window:
        return {"days_seen": 0, "min": None, "max": None, "snapshot_would_have_seen": None}
    latencies = [e["latency_ms"] for e in window]
    return {
        "days_seen": len(set(e["day"] for e in window)),
        "min": min(latencies),
        "max": max(latencies),
        "snapshot_would_have_seen": events[0]["latency_ms"] if events else None,
    }

# Evidence trail: print a sample of observations with timestamps and context
print("=== FIELD NOTES: checkout-svc ===")
print("Observation plan: 14 days in production, one event/min, deploy on day 7")
print("Named individual: checkout-svc (history: Tuesday error creep since April 12 deploy)")
print("Challenged assumption: DB is bottleneck — testing latency vs error correlation")
print("Patient action: one monitoring page per week; in a quarter the system is visible")
print()
print("Evidence trail (first 5 and last 5 observations):")
for e in events[:5] + events[-5:]:
    print(f"  {e['timestamp']} day={e['day']:2d} deploy={e['deploy']} "
          f"latency={e['latency_ms']:6.1f}ms error={e['error']}")

# Test the challenged assumption: compare Tuesday vs non-Tuesday latency and error
tue = [e for e in events if e["timestamp"][:10] in ["2026-08-04", "2026-08-11"]]
non_tue = [e for e in events if e not in tue]
tue_lat = sum(e["latency_ms"] for e in tue) / len(tue)
non_tue_lat = sum(e["latency_ms"] for e in non_tue) / len(non_tue)
tue_err = sum(e["error"] for e in tue) / len(tue)
non_tue_err = sum(e["error"] for e in non_tue) / len(non_tue)
print()
print("Challenged assumption test (Tuesday vs other days):")
print(f"  Tuesday: avg latency={tue_lat:.1f}ms, error rate={tue_err:.3f}")
print(f"  Other:   avg latency={non_tue_lat:.1f}ms, error rate={non_tue_err:.3f}")
print("  → Latency and errors rise together on Tuesdays; DB load was flat. Assumption fails.")

# Focal follow result
result = focal_follow(events, 7)
print()
print("Focal follow (days 7-14):")
print(f"  days_seen={result['days_seen']}, min={result['min']:.1f}ms, "
      f"max={result['max']:.1f}ms, snapshot_would_have_seen={result['snapshot_would_have_seen']:.1f}ms")
print("  Snapshot on day 1 would have missed the deploy-day spike and Tuesday pattern.")