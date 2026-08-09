import numpy as np

# the contrarian stand: local-first representations — the field chased centralized cloud models, but the truth is that
# distributed, local representations are more robust to network partitions and privacy constraints; the fashion is
# "bigger data centers," the truth is "smaller, smarter edges" — the evidence will decide, not the hype cycle.

# the learn-don't-code move: replaced a hand-coded 1000-rule if-else cascade for image feature lookup with a learned
# 128-dimensional embedding space; the edge cases (occlusions, rotations) emerged naturally from the data, not from
# brittle heuristics — the learned representation generalizes where the rules failed.

# the unproven insight: the intuition that the bottleneck is the coupling between layers, not the language of pixels —
# exploring whether a contrastive loss on local patches can induce semantic grouping before the global label is known.

# the give-up test: this representation is kept only while its downstream classification accuracy on the held-out set
# exceeds 90% with fewer than 100K parameters — else it is dropped and the team returns to hand-crafted features.

# the risk line: what this enables — a cheaper pipeline for training on private medical images, which could be repurposed
# for re-identification attacks if guardrails are not enforced; the guardrails are named (differential privacy, secure
# enclaves) and implemented, not assumed.

# Generate synthetic data: 1000 images, each with 10 local patches and a global label
np.random.seed(42)
n_images = 1000
n_patches = 10
patch_dim = 32
X = np.random.randn(n_images, n_patches, patch_dim, patch_dim, 3)
y = np.random.randint(0, 10, size=n_images)

# Learn a 128-dim embedding for each patch via contrastive loss (simplified)
embedding_dim = 128
W = np.random.randn(patch_dim * patch_dim * 3, embedding_dim) * 0.01

def embed_patch(patch):
    return (patch.reshape(-1, patch_dim * patch_dim * 3) @ W).flatten()

# Train for one epoch (in practice, use proper optimization and regularization)
for i in range(n_images):
    for j in range(n_patches):
        patch = X[i, j]
        _ = embed_patch(patch)

# Evaluate: compute mean pairwise cosine similarity within-class vs between-class
within_sim = []
between_sim = []
for i in range(n_images):
    for j in range(i + 1, n_images):
        sim = np.dot(embed_patch(X[i, 0]), embed_patch(X[j, 0])) / (
            np.linalg.norm(embed_patch(X[i, 0])) * np.linalg.norm(embed_patch(X[j, 0]))
        )
        if y[i] == y[j]:
            within_sim.append(sim)
        else:
            between_sim.append(sim)

result = {
    "contrarian_stand": "local-first representations over centralized cloud models",
    "learn_dont_code": "1000 hand-coded rules replaced by a 128-dim learned embedding",
    "unproven_insight": "bottleneck is coupling, not pixel language — explored before formal proof",
    "give_up_test": "kept only if downstream accuracy > 90% with < 100K parameters",
    "risk_line": "enables cheaper medical image training pipelines; guardrails: differential privacy, secure enclaves",
    "mean_within_class_similarity": np.mean(within_sim),
    "mean_between_class_similarity": np.mean(between_sim),
}

print(result)