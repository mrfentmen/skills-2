import random

# prior: sequence is fair, confidence=0.60
prior = {"label": "fair", "confidence": 0.60}
# falsifier: >= 70% heads in 100 flips would favor biased
falsifier = "evidence >= 0.70 heads would favor biased"

# probe: flip 100 coins; threshold fixed before reading them
flips = [random.choice(["H", "T"]) for _ in range(100)]
heads = sum(1 for f in flips if f == "H")
evidence = heads / len(flips)

# Update judgment
if evidence < 0.70:
    label = "fair"
    # confidence increases as evidence moves away from 0.50 toward 0.00 or 1.00
    confidence = min(0.95, 0.50 + abs(evidence - 0.50))
else:
    label = "biased"
    confidence = min(0.95, 0.50 + abs(evidence - 0.50))

judgment = {"label": label, "confidence": round(confidence, 2)}
# limitation: 100 flips cannot establish long-run bias with high certainty
limitation = "# limitation: 100 flips is a small sample for definitive bias detection"

ledger = {
    "call_id": "coin-001",
    "prediction": prior["label"],
    "evidence_n": len(flips),
    "falsifier": falsifier,
    "evidence": evidence,
    "judgment": judgment,
    "outcome": "pending"
}

print(ledger)