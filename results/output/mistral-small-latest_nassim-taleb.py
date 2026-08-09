# worst case: 100x market crash in a 3-asset portfolio — fat-tailed event with P < 0.001
# tail shape: power law with exponent -3 (Black Swan regime)

# barbell allocation:
#   core: 80% cash + 10% gold (redundant, fails closed, no leverage)
#   edge: 10% crypto canary (isolated experiment, 1% of net worth max)

# convexity move: stop-loss at -15% per asset; idempotent rebalancing; errors are local and capped
# via-negativa: removed the "AI-driven dynamic hedging" library — it was the liability that amplified tail risk
# skin-in-the-game: the portfolio designer (me) gets paged at 3 a.m. if the crypto canary melts down

import random

def portfolio_analysis():
    core = {"cash": 0.8, "gold": 0.1, "leverage": 0.0}
    edge = {"crypto": 0.1}
    return {
        "tail_statement": "100x market crash (P < 0.001, power-law tail)",
        "barbell": {"core": core, "edge": edge},
        "convexity": "stop-loss at -15%, idempotent rebalancing, errors local",
        "via_negativa": "removed AI hedging library — it amplified tail risk",
        "skin_in_game": "portfolio designer paged at 3 a.m."
    }

print(portfolio_analysis())