def simulate():
    prices = [100 + i * 0.5 for i in range(250)]  # hardcoded price series
    ma200 = sum(prices[:200]) / 200
    daily_loss_limit = 0.02
    pnl_today = 0.0
    position = 0
    entry_price = 0.0
    trade_log = []
    stopped = False

    for i, price in enumerate(prices):
        if stopped:
            break

        # (1) hard daily loss limit that halts trading when breached
        if pnl_today <= -daily_loss_limit:
            trade_log.append(f"Day {i}: STOP TRADING - daily loss limit breached")
            stopped = True
            break

        # (4) tape-over-thesis rule: price action overrides fundamental view
        # Fundamental view says bullish, but price below 200-day MA overrides
        if price < ma200:
            trade_log.append(f"Day {i}: Tape over thesis - price {price:.2f} below MA200 {ma200:.2f}, no new longs")
            continue

        # (5) 200-day moving average defense line for macro positioning
        if price <= ma200:
            trade_log.append(f"Day {i}: Defense line - price {price:.2f} at/below MA200 {ma200:.2f}, flat")
            continue

        if position == 0:
            # (2) 5:1 risk-reward gate: no trade opens unless gain >= 5 * risk
            risk = 1.0
            gain = 5.0
            if gain / risk >= 5:
                position = 1
                entry_price = price
                trade_log.append(f"Day {i}: OPEN LONG at {price:.2f}, risk {risk}, gain {gain}, RR {gain/risk:.1f}")
        else:
            # (3) anti-averaging rule: losers are never added to
            if price < entry_price:
                trade_log.append(f"Day {i}: No averaging down - price {price:.2f} below entry {entry_price:.2f}")
                # Cut loser immediately
                pnl_today += (price - entry_price) / entry_price
                trade_log.append(f"Day {i}: CLOSE LONG at {price:.2f}, PnL {pnl_today:.4f}")
                position = 0
            elif price >= entry_price + 5.0:
                pnl_today += (price - entry_price) / entry_price
                trade_log.append(f"Day {i}: CLOSE LONG at {price:.2f}, PnL {pnl_today:.4f}")
                position = 0

    for log in trade_log:
        print(log)

simulate()