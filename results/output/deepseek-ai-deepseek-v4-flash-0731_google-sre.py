SLO = 0.999
LATENCY_SLO_MS = 300
WINDOW_REQUESTS = 1_000_000

def budget_status(requests, errors, latency_samples):
    if (not isinstance(requests, int) or isinstance(requests, bool) or requests <= 0
            or not isinstance(errors, int) or isinstance(errors, bool) or not 0 <= errors <= requests
            or not isinstance(latency_samples, list)
            or any(not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0 for value in latency_samples)):
        return {"status": "invalid-metrics", "deploy_allowed": False}
    error_rate = errors / requests
    latency_good = sum(value <= LATENCY_SLO_MS for value in latency_samples)
    latency_rate = latency_good / len(latency_samples) if latency_samples else 0.0
    remaining = (1 - SLO) - error_rate
    latency_remaining = latency_rate - SLO
    deploy_allowed = remaining >= 0 and latency_remaining >= 0
    return {"status": "healthy" if deploy_allowed else "spent", "error_rate": error_rate,
            "latency_rate": latency_rate, "latency_remaining": latency_remaining,
            "remaining": remaining, "deploy_allowed": deploy_allowed}

def read_with_retry(responses, cached, max_attempts=3):
    if not isinstance(max_attempts, int) or isinstance(max_attempts, bool) or max_attempts <= 0:
        return {"status": "invalid", "value": cached, "attempts": 0, "diagnostics": []}
    if any(response not in {"ok", "throttle", "down"} for response in responses):
        return {"status": "invalid", "value": cached, "attempts": 0, "diagnostics": []}
    diagnostics = []
    for attempt, response in enumerate(responses[:max_attempts]):
        if response == "ok":
            return {"status": "full", "value": 42, "attempts": attempt + 1, "diagnostics": diagnostics}
        if response == "throttle" and attempt + 1 < max_attempts:
            diagnostics.append({"kind": "retry", "delay_ms": min(100 * (2 ** attempt) + (attempt * 17 % 31), 500)})
            continue
        return {"status": "degraded", "value": cached, "attempts": attempt + 1,
                "diagnostics": diagnostics, "reason": "dependency unavailable"}
    return {"status": "degraded", "value": cached, "attempts": min(len(responses), max_attempts),
            "diagnostics": diagnostics, "reason": "retry budget exhausted"}

# (1) SLO: 99.9% success and latency <= 300ms over a 1,000,000-request window.
#     Error budget = (1 - 0.999) * 1,000,000 = 1,000 errors allowed.
#     SLI: success rate and latency compliance rate measured over the window.

# (2) Instrumentation: budget_status aggregates request counts, error counts,
#     and latency samples into the SLI metrics. In production, counters and
#     latency buckets feed this function continuously.

# (3) Release gate: deploy_allowed is true only while both remaining error
#     budget and latency budget are non-negative. A canary is gated on this.

# (4) Fallback and retry: read_with_retry returns labeled cached data when the
#     dependency is down, with bounded attempts and exponential backoff plus
#     jitter (capped at 500ms).

# (5) Postmortem finding: "Dependency outage returned unlabeled stale data."
#     Regression check below asserts the fallback is always labeled "degraded".

healthy = budget_status(WINDOW_REQUESTS, 200, [120, 280, 290])
spent = budget_status(WINDOW_REQUESTS, 2_000, [120, 280])
invalid = budget_status(0, 0, [])
assert healthy["deploy_allowed"] and not spent["deploy_allowed"] and not invalid["deploy_allowed"]
assert read_with_retry(["throttle", "ok"], 41)["status"] == "full"
postmortem_regression = read_with_retry(["down"], 41)
assert postmortem_regression["status"] == "degraded"  # finding: fallback must be labeled
assert read_with_retry(["bogus"], 41)["status"] == "invalid"
print({"slo": "99.9% success / 1,000,000 requests", "healthy": healthy, "spent": spent, "fallback": postmortem_regression})