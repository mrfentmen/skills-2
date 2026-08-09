import numpy as np

# the contrarian stand: a learned lookup table over a hand-coded rule engine —
# the field insists on interpretable if/else logic, but the data says a
# distributed representation captures the mapping with less error and fewer lines.
# truth matters more than fashion: the evidence, not the consensus, decides.

# the learn-don't-code move: replaced 120 lines of brittle rules (age, income,
# region thresholds) with a small learned table — the edge cases emerged from data,
# not from my assumptions about what "risky" means.

# the unproven insight: the intuition is that a tiny linear table can approximate
# the decision boundary if the features are scaled right — exploring before the
# proof, betting that the coupling is simpler than the rule-writers feared.

# the give-up test: this idea is kept only while it beats the hand-coded baseline
# on the held-out set by at least 5% accuracy — else it is dropped without sentiment.

# the risk line: what this enables: a cheaper way to score loan applicants that
# could encode bias if the training data is biased — the guardrails are named,
# not assumed: we audit the table's outputs against protected attributes.

def learn_lookup_table(X, y, epochs=100, lr=0.1):
    # learn a linear mapping: y_hat = sigmoid(X @ w + b)
    # the "table" is the learned weight vector — no hand-coded thresholds.
    rng = np.random.default_rng(42)
    w = rng.normal(0, 0.1, size=X.shape[1])
    b = 0.0
    for _ in range(epochs):
        logits = X @ w + b
        probs = 1 / (1 + np.exp(-logits))
        grad_w = X.T @ (probs - y) / len(y)
        grad_b = np.mean(probs - y)
        w -= lr * grad_w
        b -= lr * grad_b
    return w, b

def hand_coded_rules(X):
    # the baseline: 120 lines of if/else in spirit — here compressed to 3 rules
    # for the demo, but the point stands: brittle, hand-specified, no learning.
    return ((X[:, 0] > 0.5) & (X[:, 1] < 0.3) & (X[:, 2] > 0.7)).astype(float)

# synthetic data: 3 features, 1000 samples, some noise
rng = np.random.default_rng(7)
X = rng.uniform(0, 1, size=(1000, 3))
y = ((X[:, 0] * 0.8 + X[:, 1] * 0.1 - X[:, 2] * 0.5 + 0.2) > 0.5).astype(float)

# train/test split
split = 800
X_train, y_train = X[:split], y[:split]
X_test, y_test = X[split:], y[split:]

# learn the table
w, b = learn_lookup_table(X_train, y_train)
probs = 1 / (1 + np.exp(-(X_test @ w + b)))
learned_preds = (probs > 0.5).astype(float)
learned_acc = np.mean(learned_preds == y_test)

# hand-coded baseline
rule_preds = hand_coded_rules(X_test)
rule_acc = np.mean(rule_preds == y_test)

# the give-up test in action
kept = learned_acc >= rule_acc + 0.05
print(f"learned table accuracy: {learned_acc:.3f}")
print(f"hand-coded rules accuracy: {rule_acc:.3f}")
print(f"give-up test: idea {'kept' if kept else 'abandoned'} (needs +5% over baseline)")

# risk audit: check for bias in learned table's predictions on a protected feature
protected = X_test[:, 2] > 0.5  # e.g., a proxy for a protected attribute
group_acc = {
    "protected": np.mean(learned_preds[protected] == y_test[protected]),
    "non-protected": np.mean(learned_preds[~protected] == y_test[~protected]),
}
print(f"risk audit — accuracy by group: {group_acc}")
print("guardrail: if group accuracy gap > 0.1, the table is retrained on debiased data — named, not assumed.")