# (1) Asymmetric-payoff statement:
# Win rate: 35%. Size when right: 3x base (press to 5x on confirmation).
# Size when wrong: 0.5x base (cut fast, thesis invalidation, not a price stop).

# (2) Concentration cap:
# Book holds max 3 high-conviction bets. No 40-name spread.
# Each bet must clear a conviction threshold >= 0.7 to be held.

# (3) Thesis-invalidation rule:
# Exit if central-bank liquidity turns (e.g., Fed balance sheet shrinks 2 consecutive months)
# OR real rates rise > 50bps in a quarter OR the macro thesis breaks (e.g., inflation re-accelerates).

# (4) Press-winners rule:
# Scale up 3-5x when the position is confirmed by both momentum (price > 50-day MA)
# AND fundamental alignment (leading liquidity signal improving) AND conviction >= 0.8.

# (5) 18-month-forward view:
# Lead with liquidity: M2 growth, Fed balance sheet trajectory, real rates, credit spreads.
# Trailing earnings are noise. Position for the liquidity cycle, not the last quarter.

# Hardcoded market data (simplified macro snapshot)
market_data = {
    "fed_balance_sheet_change_pct": -1.2,   # negative = tightening
    "real_rates_10y": 2.1,                  # percent
    "m2_growth_yoy": 3.4,                   # percent
    "credit_spread_bps": 145,               # high yield over treasuries
    "sp500_momentum": 0.03,                 # 3% above 50-day MA
    "gold_momentum": 0.08,                  # 8% above 50-day MA
    "dollar_index": 104.5,
    "inflation_breakeven_5y": 2.3,          # percent
}

# Position sizing logic
def position_size(conviction, confirmed, base=100):
    if confirmed and conviction >= 0.8:
        return base * 5          # press the winner hard
    if conviction >= 0.5:
        return base              # exploratory, small
    return 0

def should_exit(thesis_ok, liquidity_turn, pnl_anomaly):
    # never a mechanical stop: exit on invalidation
    return (not thesis_ok) or liquidity_turn or pnl_anomaly

# Analysis
liquidity_turn = market_data["fed_balance_sheet_change_pct"] < -1.0 or market_data["real_rates_10y"] > 2.5
thesis_ok = market_data["m2_growth_yoy"] > 2.0 and market_data["credit_spread_bps"] < 200
momentum_confirmed = market_data["sp500_momentum"] > 0.02 and market_data["gold_momentum"] > 0.05

# Two high-conviction bets: long gold, long equities (if liquidity supports)
gold_conviction = 0.85 if (liquidity_turn == False and market_data["gold_momentum"] > 0.05) else 0.4
equity_conviction = 0.75 if (thesis_ok and momentum_confirmed) else 0.3

gold_size = position_size(gold_conviction, momentum_confirmed)
equity_size = position_size(equity_conviction, momentum_confirmed)

# Exit checks
gold_exit = should_exit(thesis_ok, liquidity_turn, False)
equity_exit = should_exit(thesis_ok, liquidity_turn, False)

# Print analysis
print("=== DRUCKENMILLER MACRO PORTFOLIO ANALYSIS ===")
print(f"Fed balance sheet change: {market_data['fed_balance_sheet_change_pct']}%")
print(f"Real rates (10y): {market_data['real_rates_10y']}%")
print(f"M2 growth YoY: {market_data['m2_growth_yoy']}%")
print(f"Credit spreads: {market_data['credit_spread_bps']} bps")
print(f"S&P 500 momentum: {market_data['sp500_momentum']*100:.1f}% above 50-day MA")
print(f"Gold momentum: {market_data['gold_momentum']*100:.1f}% above 50-day MA")
print()
print("Liquidity turn detected:", liquidity_turn)
print("Thesis intact:", thesis_ok)
print("Momentum confirmed:", momentum_confirmed)
print()
print("--- POSITIONS ---")
print(f"Gold: conviction={gold_conviction:.2f}, size={gold_size} (base=100), exit={gold_exit}")
print(f"Equities: conviction={equity_conviction:.2f}, size={equity_size} (base=100), exit={equity_exit}")
print()
print("--- 18-MONTH FORWARD VIEW ---")
print("Leading liquidity signals: M2 growth, Fed balance sheet, real rates, credit spreads.")
print("Trailing earnings are noise. Position for the liquidity cycle.")
print("If Fed pivots to easing (balance sheet expansion), press winners 3-5x.")
print("If liquidity turns (balance sheet contraction, real rates > 2.5%), exit all.")
print()
print("--- RISK RULES ---")
print("Concentration cap: max 3 bets, only high conviction (>=0.7).")
print("Asymmetry: 35% win rate, 3x when right, 0.5x when wrong.")
print("Invalidation: exit on liquidity turn or thesis break, never a price stop.")
print("Press: scale 3-5x on confirmation (momentum + fundamentals + conviction >= 0.8).")