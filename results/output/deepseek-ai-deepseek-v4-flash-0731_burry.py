def forensic_scan(clause):
    return [flag for flag in ("covenant", "insolvency", "impairment") if flag in clause.lower()]

def thesis_artifact(ticker, clause, consensus, premium, expiry_days, liquidity, catalyst, invalidation):
    flags = forensic_scan(clause)
    if (not ticker or not flags or not consensus or premium <= 0 or expiry_days <= 0
            or liquidity not in {"high", "medium"} or not catalyst or not invalidation):
        return {"action": "PASS", "reason": "insufficient or unsafe thesis contract"}
    return {"action": "RESEARCH_ONLY_DEFINED_RISK", "ticker": ticker,
            "source_flags": flags, "consensus": consensus, "max_loss": premium,
            "expiry_days": expiry_days, "liquidity": liquidity,
            "catalyst": catalyst, "invalidation": invalidation,
            "upside": "model scenarios separately; do not invent a multiple"}

# (1) Primary-source evidence: specific contract clause cited
clause = "Indenture §4.07(b): If Consolidated EBITDA falls below $50M for two consecutive quarters, the issuer must post cash collateral equal to 120% of outstanding principal; failure to post within 30 days constitutes an Event of Default under §6.01(a)(iii)."

# (2) Market-consensus view stated and specific mispricing identified
consensus = "Consensus: bond trades at 92 cents on the dollar, market assumes covenant is non-binding because EBITDA is $60M and stable. Mispricing: the clause triggers on *Consolidated* EBITDA, which excludes the $15M non-controlling interest in the subsidiary that generates the cash; actual covenant EBITDA is $45M, already below the threshold. The market has not read the definition of 'Consolidated EBITDA' in §1.01."

# (3) Defined-risk structure: downside capped (puts / protection), upside stated
premium = 50000  # cost of long-dated put options on the bond / CDS protection
expiry_days = 730  # 2-year protection
liquidity = "medium"  # bond/CDS market liquidity
max_loss = premium  # capped at premium paid
upside = "If the covenant breach triggers default and restructuring, bond price falls to 30-40 cents; protection pays 60-70 cents per dollar notional, a 3-4x return on premium. If no breach, loss is limited to the premium."

# (4) Survival plan: how the position weathers being early (sizing, patience, evidence)
sizing = "Position sized at 2% of capital (premium_budget / total_capital = 50,000 / 2,500,000). Patience: 2-year expiry allows for the two-quarter EBITDA test to be missed; evidence log tracks quarterly EBITDA filings and covenant compliance certificates. Recheck date: 90 days before each covenant test date."

# (5) Hard-evidence thesis document: why you will not capitulate, in writing
hard_evidence = "I will not capitulate because the clause is unambiguous: §4.07(b) uses 'Consolidated EBITDA' as defined in §1.01, which explicitly excludes non-controlling interests. The last 10-Q (p. 12) shows subsidiary EBITDA of $15M attributed to the minority partner. The market's 92-cent price implies no default risk, but the covenant test is already failed. I have precommitted: I close only if (a) the issuer amends the indenture to redefine Consolidated EBITDA, or (b) the subsidiary's minority interest is bought out and EBITDA rises above $50M, or (c) the bond trades above 95 cents on a liquidity squeeze that I cannot explain. Otherwise, I hold to expiry."

report = thesis_artifact("DISTRESS-BOND-2027", clause, consensus, premium, expiry_days, liquidity,
                         "Next quarterly covenant test in 45 days; EBITDA filing due",
                         "Covenant remains compliant after amendment or minority buyout")

print("=== PRIMARY-SOURCE EVIDENCE ===")
print(clause)
print("\n=== MARKET CONSENSUS AND MISPRICING ===")
print(consensus)
print("\n=== DEFINED-RISK STRUCTURE ===")
print(f"Protection cost (max loss): ${premium}")
print(f"Expiry: {expiry_days} days")
print(f"Liquidity: {liquidity}")
print(f"Upside: {upside}")
print(f"Sizing: {sizing}")
print("\n=== SURVIVAL PLAN ===")
print(sizing)
print("Patience: 2-year expiry; evidence log tracks quarterly filings; recheck 90 days before each test.")
print("\n=== HARD-EVIDENCE THESIS (WHY I WON'T CAPITULATE) ===")
print(hard_evidence)
print("\n=== THESIS ARTIFACT ===")
print(report)
print("\nAnalytical artifact, not a trade recommendation.")