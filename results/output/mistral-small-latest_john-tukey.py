# before modeling: stem-and-leaf display and box plot summary
data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9]

# look first: quantiles and outliers
ordered = sorted(data)
n = len(ordered)
q = lambda p: ordered[int(p * (n - 1))]
iqr = q(0.75) - q(0.25)
lower_fence = q(0.25) - 1.5 * iqr
upper_fence = q(0.75) + 1.5 * iqr
outliers = [v for v in ordered if v < lower_fence or v > upper_fence]

# the real ask is "what is the central tendency and spread of this sample," not "fit a normal curve"
right_question = "what is the central tendency and spread of this sample"

# robust summary: median 5, IQR 3-7; the mean 5.1 is close but the whiskers show skew
robust_summary = {
    "median": q(0.5),
    "q1": q(0.25),
    "q3": q(0.75),
    "iqr": iqr,
    "outliers": outliers,
    "mean": sum(data) / n,
}

# 15 samples cannot support a claim about a larger population — say what the data allows
limit_note = "15 samples cannot support a claim about a larger population; describe only this sample"

# gain check: O(n log n) sort enables exact quantiles; no faster algorithmic gain needed here
gain_check = "O(n log n) sort enables exact quantiles; no faster algorithmic gain needed here"

analysis = {
    "right_question": right_question,
    "robust_summary": robust_summary,
    "limit_note": limit_note,
    "gain_check": gain_check,
}

print(analysis)