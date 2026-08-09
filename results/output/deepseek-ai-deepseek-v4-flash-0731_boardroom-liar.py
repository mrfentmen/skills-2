# (1) Persuasive founder story written before the audit:
# "Our new onboarding flow is dramatically faster, boosts activation, and users love it.
#  It will scale to any team size and cut churn in half."

# (2) Material promises converted into claims with metric, baseline, owner, sample/window, falsifier:
claims = [
    {
        "promise": "dramatically faster",
        "metric": "median_time_to_first_value_seconds",
        "baseline": 120,
        "observed": 45,
        "sample": 500,
        "window": "2-week A/B test",
        "owner": "product",
        "falsifier": "observed >= baseline",
    },
    {
        "promise": "boosts activation",
        "metric": "activation_rate_pct",
        "baseline": 30,
        "observed": 38,
        "sample": 500,
        "window": "2-week A/B test",
        "owner": "growth",
        "falsifier": "observed <= baseline",
    },
    {
        "promise": "users love it",
        "metric": "nps_score",
        "baseline": None,
        "observed": None,
        "sample": 0,
        "window": "not measured",
        "owner": "research",
        "falsifier": "nps below 40",
    },
    {
        "promise": "scale to any team size",
        "metric": "max_concurrent_users",
        "baseline": None,
        "observed": 10000,
        "sample": 1,
        "window": "single load test",
        "owner": "infra",
        "falsifier": "any saturation below 100k",
    },
    {
        "promise": "cut churn in half",
        "metric": "monthly_churn_rate_pct",
        "baseline": 5.0,
        "observed": 4.8,
        "sample": 300,
        "window": "1-month cohort",
        "owner": "success",
        "falsifier": "observed >= 2.5",
    },
]

# (3) Evidence status for every claim: supported, unsupported, or conditional
def audit(claim):
    if claim["observed"] is None or claim["sample"] == 0:
        return {**claim, "status": "unsupported", "rewrite": f"{claim['promise']} is not measured; plan: run NPS survey with n>=200 within 4 weeks"}
    if claim["promise"] == "dramatically faster":
        supported = claim["observed"] < claim["baseline"]
        return {**claim, "status": "supported" if supported else "unsupported",
                "rewrite": f"median time to first value {claim['observed']}s vs {claim['baseline']}s baseline"}
    if claim["promise"] == "boosts activation":
        supported = claim["observed"] > claim["baseline"]
        return {**claim, "status": "supported" if supported else "unsupported",
                "rewrite": f"activation {claim['observed']}% vs {claim['baseline']}% baseline"}
    if claim["promise"] == "scale to any team size":
        return {**claim, "status": "conditional",
                "rewrite": f"stable through {claim['observed']} concurrent users in {claim['sample']} load test; not 'any size'"}
    if claim["promise"] == "cut churn in half":
        # baseline 5.0, target half = 2.5; observed 4.8 is far above target
        supported = claim["observed"] <= 2.5
        return {**claim, "status": "supported" if supported else "unsupported",
                "rewrite": f"churn {claim['observed']}% vs 2.5% target (half of {claim['baseline']}%)"}

ledger = [audit(claim) for claim in claims]

# (4) Every unsupported claim rewritten as a limitation or measurement plan
# (5) Final verdict that separates the story from the evidence
print("=== ORIGINAL PITCH ===")
print("Our new onboarding flow is dramatically faster, boosts activation, and users love it. It will scale to any team size and cut churn in half.")
print("\n=== CLAIM LEDGER ===")
for entry in ledger:
    print(f"- {entry['promise']}: {entry['status']} | {entry['rewrite']} | owner={entry['owner']} | sample={entry['sample']} | window={entry['window']} | falsifier={entry['falsifier']}")

print("\n=== FINAL VERDICT ===")
print("Story says: dramatically faster, boosts activation, loved, scales to any size, churn halved.")
print("Evidence says: faster (supported), activation (supported), loved (unsupported - not measured),")
print("scales (conditional - only 10k users in one test), churn (unsupported - 4.8% vs 2.5% target).")
print("Rewrite: 'Onboarding time dropped to 45s from 120s and activation rose to 38% from 30% in a 500-user A/B test.'")
print("'We have not measured user sentiment; we plan an NPS survey. Load-tested to 10k concurrent users, not beyond.'")
print("'Churn is 4.8%, not the promised 2.5%; we need a retention program before claiming half.'")