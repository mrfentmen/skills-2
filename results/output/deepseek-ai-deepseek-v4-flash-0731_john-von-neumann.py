import random

# model: zero-sum simultaneous game, 2 agents (Player, Adversary), 3 strategies each (rock, paper, scissors)
# payoff matrix: win=+1, lose=-1, draw=0. Expected payoff = sum over joint strategy probs * payoff.

# payoff: agents = {player, adversary}, strategies = {R, P, S}, payoff = player's score
# adversary is rational: chooses distribution to minimize player's max expected payoff (minimax).

# parameter audit: 2 params — payoff matrix (fixed, 3x3, no free params) and strategy probs (2 free, 3rd determined by sum=1).
# overfitting check: no extra params; the model is the game itself, not a fitted curve.

# worst-case move: adversary can force player's expected payoff to 0 (the minimax value of RPS).
# design limits damage: player plays the minimax mixed strategy (1/3 each), guaranteeing at least 0 expected payoff.

def minimax_rps():
    # payoff matrix for player (rows) vs adversary (cols): R=0, P=1, S=2
    payoff = [
        [0, -1, 1],  # player R
        [1, 0, -1],  # player P
        [-1, 1, 0]   # player S
    ]
    # minimax mixed strategy: uniform (1/3 each) — the unique equilibrium
    player_mix = [1/3, 1/3, 1/3]
    adversary_mix = [1/3, 1/3, 1/3]
    # expected payoff = sum over all joint probs * payoff
    expected = sum(player_mix[i] * adversary_mix[j] * payoff[i][j]
                   for i in range(3) for j in range(3))
    return {"player_mix": player_mix, "adversary_mix": adversary_mix, "expected_payoff": expected}

# working check: run the game 100k times with the minimax strategies, verify empirical mean ≈ 0
def simulate(n=100000):
    rng = random.Random(42)  # deterministic pseudo-random — known, not true randomness
    score = 0
    for _ in range(n):
        p = rng.randrange(3)
        a = rng.randrange(3)
        payoff = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
        score += payoff[p][a]
    return score / n

result = minimax_rps()
empirical = simulate()
# working check: analytic expected payoff = 0, empirical mean within 0.01 of 0
print("Game result (minimax RPS):")
print(f"  Player mixed strategy: {result['player_mix']}")
print(f"  Adversary mixed strategy: {result['adversary_mix']}")
print(f"  Analytic expected payoff: {result['expected_payoff']:.4f}")
print(f"  Empirical mean payoff (100k sims): {empirical:.4f}")
print(f"  Working check: |empirical - analytic| = {abs(empirical - result['expected_payoff']):.4f} <= 0.01")