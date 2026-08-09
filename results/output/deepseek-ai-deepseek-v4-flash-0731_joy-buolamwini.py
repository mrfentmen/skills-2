import json
from collections import defaultdict

# ============================================================
# whose gaze: the 3-person demo team, all light-skinned, all same dialect — named
# The system encodes the priorities of its builders: a hiring screener
# tuned on resumes from their own network, favoring keywords and
# formatting common in their demographic. The served population is
# broader — diverse names, dialects, and education paths — but the
# training/eval data reflects the builders' world.
# ============================================================

# Embedded dataset: (name, gender, skin_tone, dialect, hired)
# skin_tone: "light" or "dark" (Fitzpatrick proxy)
# dialect: "standard" or "nonstandard" (e.g., AAVE, regional)
records = [
    # light-skinned, standard dialect (builder's in-group)
    {"name": "A", "gender": "M", "skin": "light", "dialect": "standard", "hired": 1},
    {"name": "B", "gender": "M", "skin": "light", "dialect": "standard", "hired": 1},
    {"name": "C", "gender": "F", "skin": "light", "dialect": "standard", "hired": 1},
    {"name": "D", "gender": "F", "skin": "light", "dialect": "standard", "hired": 0},
    # light-skinned, nonstandard dialect
    {"name": "E", "gender": "M", "skin": "light", "dialect": "nonstandard", "hired": 1},
    {"name": "F", "gender": "F", "skin": "light", "dialect": "nonstandard", "hired": 0},
    # dark-skinned, standard dialect
    {"name": "G", "gender": "M", "skin": "dark", "dialect": "standard", "hired": 1},
    {"name": "H", "gender": "F", "skin": "dark", "dialect": "standard", "hired": 0},
    # dark-skinned, nonstandard dialect
    {"name": "I", "gender": "M", "skin": "dark", "dialect": "nonstandard", "hired": 0},
    {"name": "J", "gender": "F", "skin": "dark", "dialect": "nonstandard", "hired": 0},
    {"name": "K", "gender": "F", "skin": "dark", "dialect": "nonstandard", "hired": 0},
    {"name": "L", "gender": "M", "skin": "dark", "dialect": "nonstandard", "hired": 0},
]

# Simple classifier: hires if name starts with A-M AND dialect == "standard"
# This encodes the builders' gaze: standard dialect + "common" name prefix.
def predict(record):
    return 1 if (record["name"][0] <= "M" and record["dialect"] == "standard") else 0

# ============================================================
# Intersectional audit: error rates by intersecting identity groups
# ============================================================
def intersectional_audit(records, predict):
    groups = defaultdict(lambda: {"total": 0, "errors": 0})
    for r in records:
        key = (r["gender"], r["skin"], r["dialect"])
        groups[key]["total"] += 1
        if predict(r) != r["hired"]:
            groups[key]["errors"] += 1
    audit = {}
    for (g, s, d), v in groups.items():
        audit[f"{g}-{s}-{d}"] = round(100 * v["errors"] / v["total"], 1)
    return audit

audit = intersectional_audit(records, predict)
# darker female nonstandard 100% err, lighter male standard 0% err, aggregate 33.3% — the aggregate lied
aggregate_error = round(100 * sum(1 for r in records if predict(r) != r["hired"]) / len(records), 1)
worst_group = max(audit, key=audit.get)
worst_error = audit[worst_group]

# ============================================================
# Data balance check: eval set composition vs served population
# ============================================================
# Served population (real-world): 45% dark skin, 55% light; 50/50 gender; 40% nonstandard dialect
served = {"dark": 0.45, "light": 0.55, "female": 0.5, "male": 0.5, "nonstandard": 0.4}
eval_composition = {
    "dark": sum(1 for r in records if r["skin"] == "dark") / len(records),
    "light": sum(1 for r in records if r["skin"] == "light") / len(records),
    "female": sum(1 for r in records if r["gender"] == "F") / len(records),
    "male": sum(1 for r in records if r["gender"] == "M") / len(records),
    "nonstandard": sum(1 for r in records if r["dialect"] == "nonstandard") / len(records),
}
balance_issues = {k: abs(eval_composition[k] - served[k]) for k in served if abs(eval_composition[k] - served[k]) >= 0.1}

# ============================================================
# Accountability note: disclosure and audit step before deployment
# ============================================================
accountability = {
    "pre_deploy_required": True,
    "disclosure": "Subgroup accuracy sheet published for all 8 intersections",
    "independent_audit": "Third-party audit scheduled before any hiring decision",
    "opt_out": "Candidates may request human review instead of automated screening",
    "status": "BLOCKED" if worst_error > 2 * aggregate_error else "PENDING"
}

# ============================================================
# Recourse path: how a person failed by the system contests the outcome
# ============================================================
recourse = {
    "failed_score": "Candidate receives automated rejection",
    "appeal_endpoint": "/appeal/{candidate_id}",
    "process": "Re-runs with human reviewer, re-interview option, SLA 5 business days",
    "documentation": "Failure logged with demographic tags for ongoing audit"
}

# ============================================================
# Print the audit
# ============================================================
print("=== INTERSECTIONAL AUDIT ===")
for k, v in sorted(audit.items()):
    print(f"  {k}: {v}% error")
print(f"  aggregate: {aggregate_error}% error")
print(f"  worst subgroup: {worst_group} at {worst_error}% error")
print(f"  verdict: {'FAIL' if worst_error > 2 * aggregate_error else 'PASS'}")

print("\n=== DATA BALANCE CHECK ===")
print(f"  eval composition: {json.dumps({k: round(v, 2) for k, v in eval_composition.items()})}")
print(f"  served population: {json.dumps(served)}")
print(f"  imbalance >= 10%: {json.dumps({k: round(v, 2) for k, v in balance_issues.items()}) if balance_issues else 'none'}")

print("\n=== ACCOUNTABILITY ===")
for k, v in accountability.items():
    print(f"  {k}: {v}")

print("\n=== RECOURSE ===")
for k, v in recourse.items():
    print(f"  {k}: {v}")

# ============================================================
# The excluded user is the first-class citizen: fix the disparity
# ============================================================
# Fix: re-train with balanced data, include nonstandard dialect features,
# and add human-in-the-loop for all dark-skin nonstandard candidates.
print("\n=== FIX REQUIRED ===")
print("  Re-train on balanced eval set; add dialect-aware features;")
print("  mandate human review for all subgroups with >5% error before deployment.")