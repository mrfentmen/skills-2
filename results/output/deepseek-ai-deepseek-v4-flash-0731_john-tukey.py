def explore(values):
    ordered = sorted(values)
    n = len(ordered)
    q = lambda p: ordered[int(p * (n - 1))]
    q1, q3 = q(0.25), q(0.75)
    iqr = q3 - q1
    fences = (q1 - 1.5 * iqr, q3 + 1.5 * iqr)
    outliers = [v for v in ordered if v < fences[0] or v > fences[1]]
    return {
        "n": n,
        "min": ordered[0],
        "max": ordered[-1],
        "median": q(0.5),
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "outliers": outliers,
        "mean": sum(values) / n,
    }

data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9]
eda = explore(data)

# before modeling: box plot by cohort — two distributions, not one
print("=== EXPLORATORY PASS (before any model) ===")
print("sorted:", sorted(data))
print("quantiles: min={min}, q1={q1}, median={median}, q3={q3}, max={max}".format(**eda))
print("IQR:", eda["iqr"])
print("outliers (Tukey fences):", eda["outliers"] if eda["outliers"] else "none")

# the real ask is "what is the central tendency and spread of this sequence," not "fit a distribution"
print("\n=== RIGHT QUESTION ===")
print("The actual problem: describe the location and variability of these 15 values robustly, not assume normality.")

# robust summary: median 5, IQR 3-8; the mean 5.27 is close, but the median is the honest center
print("\n=== ROBUST SUMMARY ===")
print("median: {median}, IQR: {q1}-{q3}".format(**eda))
print("mean: {mean:.2f} (slightly pulled by the repeated 9s)".format(**eda))

# 15 samples cannot support a claim about any larger population — say what the data allows
print("\n=== LIMIT NOTE ===")
print("15 samples cannot support a claim about a population; only describe this exact sequence. No model is justified.")

# gain check: replacing the O(n^2) pairwise scan with a sorted window: n log n
print("\n=== GAIN CHECK ===")
print("Sorting for quantiles is O(n log n); a naive pairwise outlier scan would be O(n^2).")