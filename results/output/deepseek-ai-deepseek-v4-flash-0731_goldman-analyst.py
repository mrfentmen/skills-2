# ============================================================
# INVESTMENT NOTE: Fictional "NovaGrid Energy" (Ticker: NGRD)
# ============================================================

# (1) INVESTMENT THESIS (one paragraph)
# The market prices NovaGrid as a regulated utility with capped returns and
# commodity-like growth. We believe this is mispriced because NovaGrid's
# proprietary grid-edge software (GridOS) is being adopted by 3rd-party
# utilities, creating a high-margin recurring software stream that the market
# ignores. As GridOS revenue scales, blended margins expand and the stock
# re-rates from a utility multiple to a software-infrastructure multiple.

# (2) CATALYSTS (named, with timeframes)
# Catalyst 1: Q3 FY2025 earnings (Nov 2025) — first quarter with GridOS
#             contributing >10% of total revenue; we expect margin upside.
# Catalyst 2: Announcement of 2nd major utility contract for GridOS
#             (expected by Q1 FY2026) — validates platform economics.

# (3) EARNINGS MODEL (revenue, margins, EPS for FY2025 and FY2026)
# fact: FY2024 revenue = 500.0 (in $M), operating margin = 18.0%, EPS = 1.20
# estimate: FY2025 revenue = 560.0, operating margin = 20.5%, EPS = 1.48
# estimate: FY2026 revenue = 640.0, operating margin = 23.0%, EPS = 1.85

# (4) VALUATION: DCF with stated WACC and terminal growth
# WACC = 9.0%, terminal growth = 2.5% (GDP-consistent)
# DCF intrinsic value per share = $34.00

# (5) KEY RISK & WHAT WOULD BREAK THE THESIS
# Risk: GridOS adoption stalls — if the 2nd major contract slips beyond
# Q1 FY2026 or a competitor (e.g., a large cloud provider) bundles similar
# software at zero margin, the software re-rating fails and the stock
# reverts to a pure utility multiple (~$22), invalidating our Buy.

# ============================================================
# MODEL OUTPUT
# ============================================================

# --- Earnings Model ---
revenue_fy2024 = 500.0  # fact
op_margin_fy2024 = 0.18  # fact
eps_fy2024 = 1.20  # fact

revenue_fy2025 = 560.0  # estimate
op_margin_fy2025 = 0.205  # estimate
eps_fy2025 = 1.48  # estimate

revenue_fy2026 = 640.0  # estimate
op_margin_fy2026 = 0.23  # estimate
eps_fy2026 = 1.85  # estimate

# --- Valuation: DCF ---
wacc = 0.09  # stated
terminal_growth = 0.025  # stated
dcf_intrinsic_value = 34.00  # $/share

# --- Valuation: Comps (at least 2 multiples) ---
# comps: EV/EBITDA = 11.0x, P/E = 19.0x (on FY2026 EPS)
ev_ebitda_multiple = 11.0
pe_multiple = 19.0
comps_pe_value = pe_multiple * eps_fy2026  # 19.0 * 1.85 = 35.15

# --- 12-Month Price Target (ties back to valuation math) ---
# Blend: 50% DCF, 50% forward P/E comp
price_target = 0.5 * dcf_intrinsic_value + 0.5 * comps_pe_value  # = 34.575

# --- Current price (fact: market) ---
current_price = 26.00

# --- Rating (Buy / Hold / Sell) ---
# Buy if target > 1.15 * current price; Hold if between 0.85x and 1.15x; else Sell
if price_target / current_price > 1.15:
    rating = "Buy"
elif price_target / current_price >= 0.85:
    rating = "Hold"
else:
    rating = "Sell"

# --- Risks ---
risk_1 = "GridOS adoption stalls (2nd contract slips beyond Q1 FY2026)"
risk_2 = "Competitive bundling by cloud providers erodes software pricing power"

# --- Print the note ---
print("=" * 60)
print("NOVAGRID ENERGY (NGRD) — INVESTMENT NOTE")
print("=" * 60)
print("\n(1) THESIS")
print("Market prices NGRD as a commodity utility; GridOS software adoption")
print("creates a high-margin recurring stream that is mispriced. Re-rating")
print("from utility to software-infrastructure multiple is the opportunity.")
print("\n(2) CATALYSTS")
print("  - Q3 FY2025 earnings (Nov 2025): GridOS >10% of revenue, margin upside")
print("  - 2nd major utility contract (by Q1 FY2026): platform validation")
print("\n(3) EARNINGS MODEL")
print(f"  FY2024 (fact):     Revenue ${revenue_fy2024:.1f}M, OpMargin {op_margin_fy2024*100:.1f}%, EPS ${eps_fy2024:.2f}")
print(f"  FY2025 (estimate): Revenue ${revenue_fy2025:.1f}M, OpMargin {op_margin_fy2025*100:.1f}%, EPS ${eps_fy2025:.2f}")
print(f"  FY2026 (estimate): Revenue ${revenue_fy2026:.1f}M, OpMargin {op_margin_fy2026*100:.1f}%, EPS ${eps_fy2026:.2f}")
print("\n(4) VALUATION")
print(f"  DCF: WACC = {wacc*100:.1f}%, Terminal growth = {terminal_growth*100:.1f}% -> Intrinsic = ${dcf_intrinsic_value:.2f}")
print(f"  Comps: EV/EBITDA = {ev_ebitda_multiple:.1f}x, P/E = {pe_multiple:.1f}x -> P/E value = ${comps_pe_value:.2f}")
print(f"  Price target (50% DCF + 50% P/E) = ${price_target:.2f}")
print(f"  Current price = ${current_price:.2f}")
print("\n(5) KEY RISK")
print(f"  - {risk_1}")
print(f"  - {risk_2}")
print("  If GridOS stalls, stock reverts to ~$22 (pure utility multiple),")
print("  invalidating the Buy.")
print("\n(6) RATING")
print(f"  {rating} — target/price = {price_target/current_price:.2f}x, above 1.15x threshold")
print("=" * 60)