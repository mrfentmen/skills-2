import numpy as np

def tudor_trading_simulator():
    # Hardcoded price series (simulated daily closes)
    np.random.seed(42)
    prices = np.cumprod(1 + np.random.normal(0.001, 0.02, 250)) * 100
    ma200 = np.convolve(prices, np.ones(200)/200, mode='valid')

    # Risk parameters
    DAILY_LOSS_LIMIT = 0.02  # 2% hard daily loss limit
    INITIAL_CAPITAL = 10000
    POSITION_SIZE = 0.01     # 1% of capital per trade

    # State tracking
    capital = INITIAL_CAPITAL
    pnl_today = 0
    trade_log = []
    active_trades = []
    day = 0

    while day < len(prices):
        # Daily reset
        pnl_today = 0
        day_price = prices[day]
        current_ma200 = ma200[day-199] if day >= 199 else ma200[0]

        # Hard daily loss limit check
        if capital <= INITIAL_CAPITAL * (1 - DAILY_LOSS_LIMIT):
            trade_log.append(f"Day {day}: STOP TRADING - Daily loss limit breached")
            break

        # Tape-over-thesis rule: price action overrides fundamental view
        # (In this simulation, we'll use a simple mean-reversion strategy as "fundamental view")
        fundamental_view = day_price < current_ma200  # Buy if below MA200

        # Check 200-day MA defense line
        if not fundamental_view and day >= 199:
            trade_log.append(f"Day {day}: Position rejected - price {day_price:.2f} <= MA200 {current_ma200:.2f}")
            day += 1
            continue

        # Generate random trade ideas (simulating market opportunities)
        for _ in range(np.random.randint(1, 4)):  # 1-3 trade opportunities per day
            # Simulate potential trade with random risk/reward
            risk = np.random.uniform(0.005, 0.02)  # 0.5% to 2% risk
            potential_gain = np.random.uniform(0.03, 0.10)  # 3% to 10% potential gain

            # 5:1 risk-reward gate
            if potential_gain < 5 * risk:
                continue

            # Anti-averaging rule: never add to losers
            if any(t['entry'] > day_price for t in active_trades):
                continue

            # Execute trade
            position = capital * POSITION_SIZE / day_price
            entry = day_price
            stop = entry * (1 - risk)
            target = entry * (1 + potential_gain)

            active_trades.append({
                'entry': entry,
                'stop': stop,
                'target': target,
                'position': position,
                'day': day
            })

        # Process active trades
        new_active_trades = []
        for trade in active_trades:
            # Check if trade is still active
            if day_price >= trade['stop'] or day_price <= trade['target']:
                if day_price <= trade['stop']:  # Hit stop (loss)
                    pnl = - (trade['entry'] - trade['stop']) * trade['position']
                else:  # Hit target (gain)
                    pnl = (trade['target'] - trade['entry']) * trade['position']

                capital += pnl
                pnl_today += pnl
                trade_log.append(
                    f"Day {day}: Trade closed - Entry {trade['entry']:.2f}, "
                    f"Stop {trade['stop']:.2f}, Target {trade['target']:.2f}, "
                    f"PnL {pnl:.2f}, Capital {capital:.2f}"
                )
            else:
                new_active_trades.append(trade)

        active_trades = new_active_trades
        day += 1

    # Print trade log
    for entry in trade_log:
        print(entry)

tudor_trading_simulator()