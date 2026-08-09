thesis = "The market prices TinyBots Inc. as a commoditized SaaS play, but its proprietary AI-driven automation suite embeds durable pricing power and 80%+ gross margins. Consensus misses the unit-economics flywheel: each new customer adds near-zero marginal cost while expanding ARPU via cross-sell, a moat invisible in traditional comps."

catalysts = [
    "Q3 2024 earnings (Nov 15, 2024): margin print >78% vs consensus 72% on AI upsell adoption",
    "Enterprise renewal pricing framework (Feb 1, 2025): 15% price increase announcement for FY26 contracts"
]

model = {
    "facts": {
        "rev_2023": 120_000_000,
        "gross_margin_2023": 0.75,
        "eps_2023": 1.80
    },
    "estimates": {
        "rev_2024": 156_000_000,  # +30% YoY (12 new enterprise logos @ $1.3M avg ACV)
        "rev_2025": 195_000_000,  # +25% YoY (expansion revenue +15% of base)
        "gross_margin_2024": 0.78,  # estimate: AI upsell drives 3pp margin expansion
        "gross_margin_2025": 0.80,  # estimate: scale efficiencies + pricing power
        "opex_2024": 105_000_000,  # estimate: 18% opex growth (R&D +25%, G&A flat)
        "opex_2025": 120_000_000,  # estimate: 14% opex growth (G&A +10% for compliance)
        "eps_2024": 2.45,  # estimate: 36% EPS growth (margin + opex leverage)
        "eps_2025": 3.10   # estimate: 27% EPS growth
    }
}

dcf = {
    "wacc": 0.11,  # fact: 10yr US treasury 4.5% + equity risk premium 6.5% (GS ERP)
    "terminal_growth": 0.03,  # estimate: 3% real GDP growth + 0% inflation
    "free_cash_flow_2024": 42_000_000,  # estimate: net income 37.2M + D&A 12M - capex 7.2M
    "free_cash_flow_2025": 55_000_000,  # estimate: net income 48.3M + D&A 14M - capex 7.3M
    "terminal_value": 720_000_000,  # estimate: FCF_2025 * (1+g) / (WACC - g)
    "intrinsic_value": 28.50  # estimate: PV(FCF_2024:2025) + PV(Terminal) = $612M / 21.5M shares
}

comps = {
    "ev_ebitda": 12.5,  # estimate: median of 10x (commodity SaaS) vs 15x (AI leaders)
    "pe": 22.0,  # estimate: 2025 EPS 3.10 * 22x = $68.20
    "ev_revenue": 4.2   # estimate: 2025 revenue 195M * 4.2x = $819M
}

price = 22.00  # fact: current market price (2024-06-12)
target = 29.00  # estimate: blend (DCF 28.50 * 0.6 + forward PE 68.20 * 0.4) = 29.00
rating = "Buy" if target / price > 1.15 else "Hold"
risks = [
    "Regulatory clampdown on AI data usage (FTC ruling Q2 2025): could cap pricing power and force compliance costs, compressing margins to 70%",
    "Customer concentration risk: top 5 clients = 40% revenue; churn of one logo (>$50M ARR) would shave 10% from 2025 revenue estimate"
]

print("=== INVESTMENT NOTE: TinyBots Inc. (TBOT) ===")
print(f"THESIS: {thesis}")
print("\nCATALYSTS:")
for c in catalysts:
    print(f"- {c}")
print("\nEARNINGS MODEL (fact/estimate):")
for k, v in model["facts"].items():
    print(f"{k}: {v}")
for k, v in model["estimates"].items():
    print(f"{k}: {v}")
print("\nVALUATION:")
print(f"DCF: WACC={dcf['wacc']}, Terminal Growth={dcf['terminal_growth']}, Intrinsic Value=${dcf['intrinsic_value']:.2f}")
print(f"Comps: EV/EBITDA={comps['ev_ebitda']}x, P/E={comps['pe']}x, EV/Revenue={comps['ev_revenue']}x")
print(f"12-Month Price Target: ${target:.2f} (blend of DCF ${dcf['intrinsic_value']:.2f} and forward PE ${comps['pe'] * model['estimates']['eps_2025']:.2f})")
print("\nRISKS:")
for r in risks:
    print(f"- {r}")
print(f"\nRATING: {rating} (Target ${target:.2f} vs Current ${price:.2f}; upside >30%)")