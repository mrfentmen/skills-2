import random

# prior: fair coin, confidence=0.50
# falsifier: >= 7/10 heads would make bias-toward-heads more likely
# probe: flip a fair coin 10 times; threshold fixed before reading them
observations = [random.randint(0, 1) for _ in range(10)]  # 1=heads, 0=tails
threshold = 0.70
evidence = sum(observations) / len(observations)

if evidence >= threshold:
    label = "biased-toward-heads"
    confidence = min(0.95, 0.50 + abs(evidence - threshold))
else:
    label = "fair"
    confidence = min(0.95, 0.50 + abs(evidence - 0.50))

# limitation: ten flips cannot establish a coin's true bias
ledger = {
    "call_id": "coin-001",
    "prediction": "fair",
    "confidence_prior": 0.50,
    "falsifier": ">= 7/10 heads would favor bias-toward-heads",
    "evidence_n": len(observations),
    "observed_heads": sum(observations),
    "judgment": {"label": label, "confidence": round(confidence, 2)},
    "outcome": "pending"
}
print(ledger)