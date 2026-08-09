import math
import random
from statistics import mean, stdev

# (1) Hypothesis and decision metric written before evidence is inspected:
# H1: A momentum signal (past 5-day return) predicts next-day return sign better than chance.
# Decision metric: mean next-day return in the untouched test window.
# Gate: net-of-cost mean return must be >= 0.001 (10 bps) with a 95% conservative lower bound > 0.

# (2) Named baseline and out-of-sample split:
# baseline: buy-and-hold (mean return of all days in test window)
# train: days 0-199, validation: days 200-299, test: days 300-399 (time-ordered, no shuffling)

# (3) Bias audit:
# - Leakage: signal computed only from past 5 days; test window never used in training/validation.
# - Survivorship: hardcoded synthetic series includes all days; no delisting or missing data.
# - Multiple testing: only one signal and one gate tested; no parameter search.

# (4) Result honesty: report n, standard error, and conservative 95% interval (normal approx, IID assumption stated).

# (5) Replication note:
# Run this script as-is. Random seed fixed at 42. All data is hardcoded via a deterministic generator.
# Output prints the full evaluation card. No external data or libraries beyond standard library.

random.seed(42)
n_days = 400
# Synthetic daily returns: small drift + noise, regime shift in the middle
returns = []
for i in range(n_days):
    if i < 200:
        mu = 0.0002
    elif i < 300:
        mu = 0.0005
    else:
        mu = 0.0001
    returns.append(mu + random.gauss(0, 0.01))

# Signal: sign of 5-day trailing return (1 if positive, 0 otherwise)
signal = [0] * 5
for i in range(5, n_days):
    trailing = sum(returns[i-5:i])
    signal.append(1 if trailing > 0 else 0)

# Split by time
train_returns = returns[0:200]
val_returns = returns[200:300]
test_returns = returns[300:400]
test_signal = signal[300:400]

# Baseline: buy-and-hold mean return in test
baseline = mean(test_returns)

# Strategy: follow signal (long when signal=1, flat when signal=0)
strategy_returns = [r if s == 1 else 0.0 for r, s in zip(test_returns, test_signal)]
strategy_mean = mean(strategy_returns)

# Costs: 2 bps per trade (signal change), assume turnover ~50% of days
cost_per_trade = 0.0002
turnover = sum(1 for i in range(1, len(test_signal)) if test_signal[i] != test_signal[i-1]) / len(test_signal)
cost = cost_per_trade * turnover
net_mean = strategy_mean - cost

# Standard error (IID approximation; real dependence would need HAC or block bootstrap)
n = len(strategy_returns)
se = stdev(strategy_returns) / math.sqrt(n) if n > 1 else None
conservative_lower = net_mean - 1.96 * se if se is not None else net_mean

# Verdict: predeclared gate is net_mean >= 0.001 AND conservative lower bound > 0
verdict = "PASS" if (net_mean >= 0.001 and conservative_lower > 0) else "REJECT"

print("=== QUANT RESEARCH DEMO ===")
print("Hypothesis: momentum signal improves next-day return vs buy-and-hold")
print("Metric: mean next-day return in untouched test window")
print("Gate: net mean >= 0.001 and 95% conservative lower bound > 0")
print()
print("Baseline (buy-and-hold test mean):", round(baseline, 6))
print("Strategy gross mean:", round(strategy_mean, 6))
print("Cost (2bps * turnover):", round(cost, 6))
print("Net mean after cost:", round(net_mean, 6))
print("Test n:", n)
print("Standard error (IID approx):", round(se, 6) if se else None)
print("Conservative 95% lower bound:", round(conservative_lower, 6))
print("Turnover:", round(turnover, 4))
print()
print("Bias audit:")
print("- Leakage: signal uses only past 5 days; test window untouched in training/validation")
print("- Survivorship: synthetic series includes all days; no delisting or missing data")
print("- Multiple testing: one signal, one gate; no parameter search")
print()
print("Replication: run this script as-is; seed=42, deterministic generator, standard library only")
print()
print("VERDICT:", verdict)