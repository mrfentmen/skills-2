# checklist: 5 critical steps only
# 1) secrets rotated
# 2) migration idempotent
# 3) rollback verified
# 4) on-call named
# 5) metrics up
# rule: if it does not catch a real failure, prune it

# pause point: cutover timeout
# everyone states their name and role, then:
# "rollback tested? backups verified?"

# classification: simple — recipe-like, no expert subsystems needed
# dictates: follow the list verbatim; no improvisation under pressure

# co-creation: the release team ran it 3 times; step 4 caught nothing twice — pruned

# discipline: even experts follow the list because memory and attention fail under pressure

def deployment_checklist():
    return {
        "items": [
            "secrets rotated",
            "migration idempotent",
            "rollback verified",
            "on-call named",
            "metrics up"
        ],
        "n": 5,
        "pause_point": {
            "roles": ["dev", "ops", "qa"],
            "verify": ["rollback tested", "backups verified"]
        },
        "classification": "simple: recipe, no subsystems",
        "failure_target": "skipping secrets rotation or rollback test"
    }

print(deployment_checklist())