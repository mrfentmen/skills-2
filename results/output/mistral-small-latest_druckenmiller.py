def macro_portfolio_analysis():
    # Asymmetric-payoff statement:
    # Win rate: 30% (3 out of 10 trades hit the macro thesis)
    # Size when right: 5x base (500 units)
    # Size when wrong: 1x base (100 units)
    # Max loss per trade: 1% of portfolio (risk budget)

    # Concentration cap:
    # Book holds 1-2 high-conviction bets at any time
    # No more than 3 active positions in a year

    # Thesis-invalidation rule:
    # Exit if: (a) central bank policy shift contradicts thesis OR
    #          (b) real rates move 150bps against thesis OR
    #          (c) daily P&L anomaly > 2% of position size

    # Press-winners rule:
    # Scale position 3-5x when: (a) thesis confirmed by 2+ leading indicators AND
    #                           (b) liquidity conditions align AND
    #                           (c) real rates move in thesis direction

    # 18-month-forward view:
    # Lead with: (1) central bank balance sheet projections, (2) real rate forecasts,
    #            (3) credit impulse signals, (4) commodity inventory trends
    # Ignore: trailing earnings, recent GDP prints, or lagging indicators

    # Hardcoded market data (simplified)
    market_data = {
        'central_bank_balance_sheet_growth': 0.05,  # 5% YoY
        'real_rates_10y': 0.012,                   # 1.2%
        'credit_impulse': 0.03,                    # 3% of GDP
        'commodity_inventory_change': -0.02,       # -2% YoY
        'daily_pnl_anomaly': 0.005,                 # 0.5% of position
        'thesis_confirmed_by_indicators': 2,        # 2 confirming indicators
        'real_rates_direction': 'down'              # real rates falling
    }

    # Position sizing logic
    base_size = 100
    conviction = 0.85  # High conviction based on research

    # Press winners condition
    if (market_data['thesis_confirmed_by_indicators'] >= 2 and
        market_data['real_rates_direction'] == 'down'):
        size = base_size * 5
        press_winner = True
    else:
        size = base_size
        press_winner = False

    # Thesis invalidation check
    thesis_ok = (
        market_data['central_bank_balance_sheet_growth'] > 0.03 and
        market_data['real_rates_10y'] < 0.02 and
        market_data['credit_impulse'] > 0.01 and
        abs(market_data['commodity_inventory_change']) < 0.05
    )
    liquidity_turn = market_data['central_bank_balance_sheet_growth'] < 0.01
    pnl_anomaly = market_data['daily_pnl_anomaly'] > 0.02

    should_exit_flag = not thesis_ok or liquidity_turn or pnl_anomaly

    # Portfolio analysis output
    analysis = {
        'asymmetric_payoff': {
            'win_rate': 0.3,
            'size_when_right': 500,
            'size_when_wrong': 100,
            'max_loss_per_trade_pct': 0.01
        },
        'concentration_cap': {
            'max_positions': 2,
            'max_active_positions_per_year': 3
        },
        'thesis_invalidation_rule': {
            'central_bank_policy_shift': 'balance_sheet_growth < 3%',
            'real_rates_move': '>150bps against thesis',
            'daily_pnl_anomaly': '>2% of position'
        },
        'press_winners_rule': {
            'confirmation_requirements': '2+ leading indicators',
            'liquidity_conditions': 'credit impulse >1% GDP',
            'real_rates_direction': 'moving in thesis direction'
        },
        'forward_view': {
            'leading_indicators': [
                'central_bank_balance_sheet_projections',
                'real_rate_forecasts',
                'credit_impulse_signals',
                'commodity_inventory_trends'
            ],
            'ignored_indicators': [
                'trailing_earnings',
                'recent_GDP_prints',
                'lagging_macro_data'
            ]
        },
        'current_position': {
            'size': size,
            'conviction': conviction,
            'press_winner': press_winner,
            'thesis_valid': thesis_ok,
            'should_exit': should_exit_flag
        }
    }

    return analysis

analysis = macro_portfolio_analysis()
print(analysis)