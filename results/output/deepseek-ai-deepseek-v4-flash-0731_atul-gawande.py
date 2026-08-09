def checklist(items):
    # 5-9 critical steps only: respect working memory, catch what is easy to miss
    keep = [i for i in items if i.get("critical")][:9]
    return {"items": [i["step"] for i in keep],
            "n": len(keep),
            "rule": "if it does not catch a real failure, prune it"}

def pause_point(roles, constraints):
    # the timeout: name every role, verify the critical constraints out loud
    return {"named_roles": roles, "verified_out_loud": constraints,
            "go": all(c.get("confirmed") for c in constraints)}

# 1) checklist: 5-9 items covering the critical, easily-missed steps only
# 1) secrets rotated 2) migration idempotent 3) rollback verified 4) on-call named 5) metrics up
# 6) healthcheck green 7) feature flag off 8) logs streaming 9) backup restored
deploy_steps = [
    {"step": "secrets rotated", "critical": True},
    {"step": "migration idempotent", "critical": True},
    {"step": "rollback verified", "critical": True},
    {"step": "on-call named", "critical": True},
    {"step": "metrics up", "critical": True},
    {"step": "healthcheck green", "critical": True},
    {"step": "feature flag off", "critical": True},
    {"step": "logs streaming", "critical": True},
    {"step": "backup restored", "critical": True},
    {"step": "style polish", "critical": False},
]

# 2) pause point: an explicit stop-and-verify moment with roles named
# cutover timeout: everyone states their name and role, then: "rollback tested? backups verified?"
cutover = pause_point(
    ["db", "app", "release"],
    [
        {"c": "migration idempotent", "confirmed": True},
        {"c": "rollback verified", "confirmed": True},
        {"c": "backup restored", "confirmed": True},
    ]
)

# 3) problem classification: simple, complicated, or complex — and what that dictates
# complex: 6 services, shared state, unknown interactions — push authority to the edge, handoffs explicit

# 4) co-creation note: the checklist field-tested and pruned with its users
# the release team ran it 3 times; step 4 caught nothing twice — pruned

# 5) discipline note: why even experts follow the list
# the knowledge exists; memory and attention fail under pressure — the list is the safety net

result = checklist(deploy_steps)
print("Deployment Checklist:")
for i, step in enumerate(result["items"], 1):
    print(f"  {i}) {step}")
print(f"Total critical steps: {result['n']}")
print(f"Pause point roles: {cutover['named_roles']}")
print(f"Pause point verified: {cutover['verified_out_loud']}")
print(f"Go: {cutover['go']}")