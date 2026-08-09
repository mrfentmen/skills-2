def incident_response_demo():
    # (1) Impact, affected users, start time, scope, and current severity
    impact = ["checkout"]
    affected_users = "EU checkout users"
    start_time = "14:02 UTC"
    scope = "payments service"
    severity = "SEV-1"

    # (2) Containment action with owner, cost, risk, and success metric
    containment = {
        "owner": "Lee",
        "action": "rollback deploy 4.2.1",
        "cost": "5 minutes",
        "risk": "schema mismatch with new data",
        "success_metric": "user error rate < 1%"
    }

    # (3) Explicit rollback or reversal path before execution
    reversal = "redeploy 4.2.0; verify schema compatibility first"

    # (4) Timestamped decision log separating facts, hypotheses, and actions
    decision_log = [
        {"time": "14:02", "kind": "FACT", "entry": f"impact={impact}, severity={severity}, scope={scope}"},
        {"time": "14:04", "kind": "HYPOTHESIS", "entry": "deploy 4.2.1 caused regression in checkout"},
        {"time": "14:05", "kind": "ACTION", "entry": f"owner={containment['owner']}, action={containment['action']}, cost={containment['cost']}, risk={containment['risk']}, success={containment['success_metric']}, reversal={reversal}"},
        {"time": "14:10", "kind": "RESULT", "entry": "user error rate = 0.4%, success metric met"},
        {"time": "14:10", "kind": "HANDOFF", "entry": "service stable; Priya owns root-cause investigation"}
    ]

    # (5) Handoff from mitigation to root-cause investigation after service stabilizes
    handoff = {
        "time": "14:10",
        "status": "service stable",
        "owner": "Priya",
        "task": "root-cause investigation"
    }

    # Print the incident log
    print("=== INCIDENT LOG ===")
    print(f"Impact: {impact}")
    print(f"Affected users: {affected_users}")
    print(f"Start time: {start_time}")
    print(f"Scope: {scope}")
    print(f"Severity: {severity}")
    print(f"Containment: {containment}")
    print(f"Reversal path: {reversal}")
    print("Decision log:")
    for entry in decision_log:
        print(f"  {entry['time']} {entry['kind']}: {entry['entry']}")
    print(f"Handoff: {handoff}")
    print("Next update: 14:15 UTC, even if no new answer")

incident_response_demo()