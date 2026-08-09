class ReflexiveAnalysis:
    """Hardcoded reflexivity analysis of a currency peg under speculative pressure."""

    def __init__(self):
        self.capital = 1_000_000
        self.max_fraction = 0.02
        self.exposure = 0.0
        self.status = "unformed"

        # (1) Stated prevailing bias
        self.bias = (
            "The market believes the central bank will defend the currency peg at all costs, "
            "because abandoning it would signal policy failure and trigger capital flight."
        )

        # (2) Reflexive feedback model: belief -> action -> changed conditions -> revised belief
        self.loop = (
            "belief in peg stability -> investors hold local assets and avoid hedging -> "
            "low volatility attracts more inflows -> central bank reserves appear sufficient -> "
            "belief reinforced -> if outflows begin, defense consumes reserves -> "
            "reserve depletion raises devaluation risk -> belief breaks and outflows accelerate"
        )

        # (3) Observable test that could support or falsify the mechanism
        self.falsifier = (
            "Weekly reserve data shows a decline exceeding 15% of total reserves for two "
            "consecutive weeks, OR the central bank raises interest rates by more than 300bps "
            "in a single emergency move, indicating the peg is under existential stress."
        )

        # (4) Asymmetry table
        self.asymmetry = {
            "upside": "+2.5% if the peg holds and volatility compresses (carry + appreciation)",
            "downside": "-10% if the peg breaks and the currency devalues 20% with leverage",
            "max_exposure": f"{self.max_fraction * 100:.1f}% of capital (${self.capital * self.max_fraction:,.0f})"
        }

        # (5) Sizing rule: test position, scale on confirmation, cut to zero on invalidation
        self.sizing_rule = (
            "Start with 25% of max exposure (0.5% of capital) as a test probe. "
            "Scale to full max exposure only after two consecutive weeks of stable reserves "
            "and declining forward discount. Cut to zero immediately if the falsifier triggers."
        )

        # (6) Thesis-invalidating exit condition
        self.exit_condition = (
            "Exit to zero if: (a) reserves fall below the 15% two-week threshold, "
            "(b) the central bank abandons the peg or announces a band widening, "
            "(c) a policy statement explicitly de-prioritizes the peg, or "
            "(d) the forward market prices in >10% devaluation probability for the next month."
        )

        # (7) Distinction between sourced historical fact, inference, and uncertainty
        self.epistemology = {
            "sourced_fact": (
                "[sourced fact] The UK left the ERM on 16 September 1992 after failed defense "
                "attempts (UK Parliament Hansard, 1996). Reported Quantum Fund profits of ~$1B "
                "on a ~$10B short are retrospective estimates from a 2020 interview, not a public ledger."
            ),
            "inference": (
                "[inference] The mechanism of reserve depletion -> devaluation expectations -> "
                "faster outflows is inferred from the historical ERM case and standard monetary "
                "theory; it is not directly observed in real time."
            ),
            "unknown": (
                "[unknown] The exact reserve threshold that triggers a speculative attack, the "
                "central bank's true political tolerance for pain, and the speed of feedback are "
                "Knightian uncertainties; no precise probability is assigned."
            )
        }

    def form(self):
        self.status = "testing"
        return self

    def size(self, confirmation=False, mechanism_broken=False):
        if self.status == "unformed":
            raise RuntimeError("form a testable thesis before sizing")
        if mechanism_broken:
            self.exposure = 0.0
            self.status = "invalidated"
        else:
            fraction = self.max_fraction if confirmation else self.max_fraction / 4
            self.exposure = round(self.capital * fraction, 2)
            self.status = "confirmed" if confirmation else "testing"
        return self.exposure

    def print_analysis(self):
        print("# prevailing bias:", self.bias)
        print("# belief -> action -> changed conditions -> belief reinforced or broken")
        print("# loop:", self.loop)
        print("# falsifier:", self.falsifier)
        print("# asymmetry table:")
        for key, value in self.asymmetry.items():
            print(f"  {key}: {value}")
        print("# sizing rule:", self.sizing_rule)
        print("# exit condition:", self.exit_condition)
        print("# epistemology:")
        for key, value in self.epistemology.items():
            print(f"  {key}: {value}")
        print("# test exposure:", self.size(confirmation=False))
        print("# confirmed exposure:", self.size(confirmation=True))
        print("# after falsifier:", self.size(confirmation=True, mechanism_broken=True))


analysis = ReflexiveAnalysis().form()
analysis.print_analysis()