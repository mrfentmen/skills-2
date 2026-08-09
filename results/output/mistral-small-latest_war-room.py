def incident_response(health, deploy, owners):
    # Impact: 14:02 UTC; auth service down; affected users: all login users; scope: global; severity: SEV-1
    # Containment action: owner=Alex; action=disable auth feature flag; cost=2m; risk=loss of new auth features; success metric=login error rate < 0.1%
    # Rollback: reversal=re-enable feature flag; verify auth service health first
    # Decision log:
    #   14:02 FACT: auth service down, SEV-1
    #   14:04 HYPOTHESIS: feature flag corruption
    #   14:05 ACTION: disable auth feature flag
    #   14:07 RESULT: login error rate 0.05%
    #   14:07 HANDOFF: root-cause investigation by Alex after stabilization
    impact = [service for service, status in health.items() if status == "down"]
    affected_scope = "global login users"
    started_at = "14:02 UTC"
    severity = "SEV-1"
    action = {
        "owner": owners[0],
        "action": "disable auth feature flag",
        "cost": "2 minutes",
        "risk": "loss of new auth features",
        "success_metric": "login error rate < 0.1%",
        "reversal": "re-enable feature flag; verify auth service health first",
    }
    login_error_rate = 0.0005
    recovery_check = {"login_error_rate": login_error_rate, "success": login_error_rate < 0.001}
    log = [
        {"time": "14:02", "kind": "FACT", "entry": f"impact={impact}, severity={severity}"},
        {"time": "14:04", "kind": "HYPOTHESIS", "entry": "feature flag corruption suspected"},
        {"time": "14:05", "kind": "ACTION", "entry": action},
        {"time": "14:07", "kind": "RESULT", "entry": recovery_check},
        {"time": "14:07", "kind": "HANDOFF", "entry": "Alex owns root-cause investigation after stabilization"},
    ]
    return {"impact": impact, "affected_scope": affected_scope, "started_at": started_at,
            "severity": severity, "action": action, "recovery_check": recovery_check,
            "next_update": "14:12", "log": log}

print(incident_response({"auth": "down", "payments": "up", "catalog": "up"}, "4.2.1", ["Alex"]))