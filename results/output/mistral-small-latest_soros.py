class ReflexiveAnalysis:
    """A bounded reflexivity analysis; it is an analysis aid, not a trading system."""

    def __init__(self):
        self.analysis = None

    def analyze(self):
        # prevailing bias: the market believes the US dollar will remain the dominant global reserve currency indefinitely due to network effects and liquidity depth [sourced fact: IMF COFER data shows USD reserves at ~60% in 2023, but this is a snapshot, not a trend]
        # belief -> action: investors overweight USD assets for safety and liquidity -> changed conditions: deep USD markets reinforce confidence -> revised belief: the USD's dominance is self-sustaining [inference]
        # [falsifier]: a sustained shift in central bank allocations away from USD or a credible alternative reserve asset emerges (e.g., digital currency, commodity-backed unit)
        # [unknown]: the timing and catalyst for such a shift; the elasticity of reserve demand to geopolitical shocks

        # observable test: monitor IMF COFER data quarterly for directional changes in USD reserve share; a 3-quarter decline of >5 percentage points would falsify the prevailing bias [sourced fact: COFER is published quarterly with a 6-month lag]
        # asymmetry table:
        #   if right: USD dominance persists -> liquidity premium preserved, capital gains from USD-denominated assets [inference]
        #   if wrong: USD reserve share declines -> capital losses on USD assets, potential liquidity crunch [inference]
        #   max exposure: 5% of capital to USD-denominated assets (e.g., Treasuries, cash) [inference]
        # sizing rule: start with 1% exposure; scale to 5% only if COFER shows USD reserve share >60% for 2 consecutive quarters [inference]
        # thesis-invalidating exit: COFER data shows USD reserve share <55% in a single quarter [sourced fact: COFER granularity is 5% bands]
        # distinction:
        #   [sourced fact]: IMF COFER data, USD reserve share ~60% in 2023
        #   [inference]: network effects and liquidity depth sustain USD dominance
        #   [unknown]: the speed and catalyst for reserve diversification

        self.analysis = {
            "prevailing_bias": "the market believes the US dollar will remain the dominant global reserve currency indefinitely due to network effects and liquidity depth [sourced fact: IMF COFER data shows USD reserves at ~60% in 2023, but this is a snapshot, not a trend]",
            "reflexive_feedback": "belief in USD dominance -> investors overweight USD assets for safety and liquidity -> deep USD markets reinforce confidence -> revised belief: the USD's dominance is self-sustaining [inference]",
            "observable_test": "monitor IMF COFER data quarterly for directional changes in USD reserve share; a 3-quarter decline of >5 percentage points would falsify the prevailing bias [sourced fact: COFER is published quarterly with a 6-month lag]",
            "asymmetry_table": {
                "if_right": "USD dominance persists -> liquidity premium preserved, capital gains from USD-denominated assets [inference]",
                "if_wrong": "USD reserve share declines -> capital losses on USD assets, potential liquidity crunch [inference]",
                "max_exposure": "5% of capital to USD-denominated assets (e.g., Treasuries, cash) [inference]"
            },
            "sizing_rule": "start with 1% exposure; scale to 5% only if COFER shows USD reserve share >60% for 2 consecutive quarters [inference]",
            "exit_condition": "COFER data shows USD reserve share <55% in a single quarter [sourced fact: COFER granularity is 5% bands]",
            "distinction": {
                "sourced_fact": "IMF COFER data, USD reserve share ~60% in 2023",
                "inference": "network effects and liquidity depth sustain USD dominance",
                "unknown": "the speed and catalyst for reserve diversification"
            }
        }
        return self.analysis

analysis = ReflexiveAnalysis().analyze()
for key, value in analysis.items():
    print(f"{key}:")
    if isinstance(value, dict):
        for subkey, subvalue in value.items():
            print(f"  {subkey}: {subvalue}")
    else:
        print(f"  {value}")