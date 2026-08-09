# PERSUASIVE FOUNDER STORY (pre-audit)
# "Our AI-powered customer support bot will slash response times to near-zero, handle 100% of inquiries automatically, and cut support costs by 90% within six months. Users will love it so much they’ll never want to speak to a human again."

pitch = "Our AI-powered customer support bot will slash response times to near-zero, handle 100% of inquiries automatically, and cut support costs by 90% within six months. Users will love it so much they’ll never want to speak to a human again."

# CLAIM LEDGER: each material promise converted into a falsifiable claim
claims = [
    # Claim 1: "slash response times to near-zero"
    {
        "text": "slash response times to near-zero",
        "metric": "avg_response_ms",
        "baseline": 12000,  # 12 seconds (industry baseline for human support)
        "observed": 150,    # measured in pilot
        "sample": 5000,     # 5000 support interactions
        "window": "pilot_30d",
        "owner": "ai_engineering",
        "falsifier": ">= baseline"
    },
    # Claim 2: "handle 100% of inquiries automatically"
    {
        "text": "handle 100% of inquiries automatically",
        "metric": "automation_rate_pct",
        "baseline": 0,      # no automation before
        "observed": 85,     # measured in pilot
        "sample": 5000,     # 5000 support interactions
        "window": "pilot_30d",
        "owner": "ai_engineering",
        "falsifier": "< 100"
    },
    # Claim 3: "cut support costs by 90%"
    {
        "text": "cut support costs by 90%",
        "metric": "cost_per_interaction_usd",
        "baseline": 12.50,  # $12.50 per human interaction
        "observed": 1.80,   # measured in pilot
        "sample": 5000,     # 5000 support interactions
        "window": "pilot_30d",
        "owner": "finance",
        "falsifier": ">= baseline * 0.10"  # i.e., not a 90% reduction
    },
    # Claim 4: "users will love it so much they’ll never want to speak to a human again"
    {
        "text": "users will love it so much they’ll never want to speak to a human again",
        "metric": "csat_5star_pct",
        "baseline": None,   # no baseline (new metric)
        "observed": None,   # not measured yet
        "sample": 0,        # no sample collected
        "window": "not measured",
        "owner": "product",
        "falsifier": "csat < 90%"
    }
]

def audit_claim(claim):
    # Evidence status classification
    if claim["observed"] is None or claim["sample"] == 0:
        return {
            **claim,
            "status": "unsupported",
            "rewrite": f"{claim['text']} is not measured; plan: run 30-day CSAT survey with {claim['sample'] or 1000} users"
        }
    if claim["metric"] == "avg_response_ms":
        is_supported = claim["observed"] < claim["baseline"]
        return {
            **claim,
            "status": "supported" if is_supported else "unsupported",
            "rewrite": f"avg response time reduced to {claim['observed']}ms from {claim['baseline']}ms baseline ({claim['observed']/claim['baseline']:.1%} of baseline)"
        }
    if claim["metric"] == "automation_rate_pct":
        is_supported = claim["observed"] >= 100
        return {
            **claim,
            "status": "supported" if is_supported else "unsupported",
            "rewrite": f"automation rate was {claim['observed']}% vs 100% target (not achieved)"
        }
    if claim["metric"] == "cost_per_interaction_usd":
        reduction_pct = (1 - (claim["observed"] / claim["baseline"])) * 100
        is_supported = reduction_pct >= 90
        return {
            **claim,
            "status": "supported" if is_supported else "unsupported",
            "rewrite": f"cost reduced to ${claim['observed']:.2f} from ${claim['baseline']:.2f} baseline ({reduction_pct:.1f}% reduction vs 90% target)"
        }
    return {
        **claim,
        "status": "conditional",
        "rewrite": f"{claim['text']} observed at {claim['observed']} with {claim['sample']} interactions; next: expand to 50k interactions over 90 days"
    }

# Audit all claims
ledger = [audit_claim(claim) for claim in claims]

# Final verdict: separate story from evidence
final_pitch = " ".join([entry["rewrite"] for entry in ledger if entry["status"] in ["supported", "conditional"]])

# Print audit
print({
    "original_pitch": pitch,
    "claim_ledger": ledger,
    "final_pitch": final_pitch
})