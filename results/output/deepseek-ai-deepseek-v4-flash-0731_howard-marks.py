def investment_memo():
    # (1) second-level pass: consensus is pricing in "AI infrastructure is a sure thing"
    # hidden cost: the capex cycle turns, and the marginal dollar of compute gets commoditized
    consensus = "AI infrastructure is a sure thing"
    priced_in = "everyone's growth forecast already assumes 40%+ CAGR forever"
    hidden_cost = "when the buildout overshoots, utilization drops and pricing power vanishes"

    # (2) risk-location note: the risk is least perceived in the "safe" mega-cap names
    # that everyone agrees are defensive; the actual risk is their valuation multiple
    risk_location = "the risk is in the 'safe' mega-cap AI names, not the speculative small caps"

    # (3) preparation move: harden for an outlier that cannot be predicted — a sudden
    # repricing of the whole complex; position with cash and a barbell, not a single bet
    preparation = "hold 20% cash, keep a barbell of short-duration bonds and deep-value cyclicals"

    # (4) temperature reading: the room is euphoric; every fund letter mentions AI
    # this is the time to question, not to add; fear is absent, which is the warning
    temperature = "euphoria: AI is in every pitch deck; implies we should be reducing, not chasing"

    # (5) price-vs-value audit: the total cost of ownership of owning the consensus
    # trade is the multiple compression when growth normalizes; the value is the
    # eventual cash flows, which are already discounted at perfection
    price = "entry at 35x forward earnings + 2% annual dilution + opportunity cost"
    value = "underlying cash flow growth of 15% if the buildout works as planned"
    buy = value > price  # false — the price already pays for the value and then some

    memo = f"""
    INVESTMENT MEMO — HARDCODED EXAMPLE
    ===================================
    (1) SECOND-LEVEL PASS
        Consensus: {consensus}
        Priced in: {priced_in}
        Hidden cost: {hidden_cost}

    (2) RISK LOCATION
        {risk_location}

    (3) PREPARATION MOVE
        {preparation}

    (4) TEMPERATURE READING
        {temperature}

    (5) PRICE-VS-VALUE AUDIT
        Price (total cost of ownership): {price}
        Value (what you get): {value}
        Buy? {buy} — avoid the losers; the winners take care of themselves.
    """
    print(memo)

investment_memo()