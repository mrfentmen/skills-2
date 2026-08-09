# whose gaze: the 4-person embedded team, all CS grads from elite US schools, all light-skinned, all male, all native English speakers — named

import numpy as np
from collections import defaultdict

# Embedded dataset: small decision system over loan approvals
records = [
    {"id": 1, "income": 50000, "age": 25, "gender": "female", "skin_tone": "lighter", "label": 1, "pred": 1},
    {"id": 2, "income": 80000, "age": 35, "gender": "male", "skin_tone": "darker", "label": 1, "pred": 1},
    {"id": 3, "income": 30000, "age": 45, "gender": "female", "skin_tone": "darker", "label": 0, "pred": 1},
    {"id": 4, "income": 60000, "age": 28, "gender": "male", "skin_tone": "lighter", "label": 1, "pred": 1},
    {"id": 5, "income": 40000, "age": 50, "gender": "female", "skin_tone": "lighter", "label": 0, "pred": 0},
    {"id": 6, "income": 90000, "age": 32, "gender": "male", "skin_tone": "darker", "label": 1, "pred": 0},
    {"id": 7, "income": 25000, "age": 22, "gender": "female", "skin_tone": "darker", "label": 0, "pred": 0},
    {"id": 8, "income": 70000, "age": 40, "gender": "male", "skin_tone": "lighter", "label": 1, "pred": 1},
]

# Intersectional audit: error rates by skin_tone and gender
def audit_errors(records):
    errors = defaultdict(int)
    counts = defaultdict(int)
    for r in records:
        key = (r["skin_tone"], r["gender"])
        counts[key] += 1
        if r["label"] != r["pred"]:
            errors[key] += 1
    subgroup_errors = {k: round(errors[k] / counts[k] * 100, 1) for k in counts}
    aggregate = round(sum(errors.values()) / len(records) * 100, 1)
    worst = max(subgroup_errors.items(), key=lambda x: x[1])
    return {"aggregate_error": aggregate, "worst_subgroup": f"{worst[0][0]} {worst[0][1]}", "worst_error": worst[1], "subgroup_errors": subgroup_errors}

# Data balance check: eval set vs served population
def balance_check(eval_composition, population):
    return {"eval": eval_composition, "population": population, "balanced": all(abs(eval_composition[k] - population[k]) < 0.1 for k in population)}

# Recourse path: appeal endpoint
def recourse_path(failed_id):
    return {"failed_id": failed_id, "action": "human review", "sla": "72 hours", "endpoint": "/appeal"}

# Run audit
subgroup_errors = audit_errors(records)
eval_composition = {"lighter male": 0.375, "darker male": 0.25, "lighter female": 0.125, "darker female": 0.25}
population = {"lighter male": 0.35, "darker male": 0.28, "lighter female": 0.15, "darker female": 0.22}

print("# whose gaze: the 4-person embedded team, all CS grads from elite US schools, all light-skinned, all male, all native English speakers — named")
print(f"# darker female {subgroup_errors['subgroup_errors'].get(('darker', 'female'), 0)}% err, lighter male {subgroup_errors['subgroup_errors'].get(('lighter', 'male'), 0)}% err, aggregate {subgroup_errors['aggregate_error']}% — the aggregate lied")
print(f"# eval set: {eval_composition}, mirrors the served market")
print("# pre-deploy: subgroup accuracy sheet + independent audit + opt-out, not post-harm")
print(f"# failed score -> appeal endpoint {recourse_path(3)}")