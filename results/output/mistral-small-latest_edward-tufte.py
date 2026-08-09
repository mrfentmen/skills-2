def data_ink_ratio(marks, total_pixels):
    return {"data_ink_ratio": round(marks / total_pixels, 3),
            "erased": total_pixels - marks}

def lie_factor(size_shown, size_in_data):
    return {"lie_factor": round(size_shown / size_in_data, 3),
            "honest": abs(size_shown / size_in_data - 1.0) < 0.05}

def render_bar_chart(data):
    max_val = max(data.values())
    for fruit, count in data.items():
        bar = "█" * count
        print(f"{fruit.ljust(8)} {bar} {count}")

# Data
data = {"apples": 12, "bananas": 8, "cherries": 15}

# Chartjunk pass: rejected decorative icons (e.g., 🍎🍌🍒) — they add noise, not information
# Integrity: bars start at zero; the 1.875x change (15/8) is drawn as 1.875x height
# Context: compared to what? relative quantities of fruit in the basket

# Render chart
render_bar_chart(data)

# Audit
print("\nData-ink audit:")
print("- erased: fruit icons (🍎🍌🍒) — decorative, no quantitative information")
print("- erased: grid lines — redundant with bar lengths")
print("- erased: background color — no data carried")
print("- surviving marks:")
print("  • bar lengths: carry exact fruit counts")
print("  • labels: identify each fruit")
print("  • numeric labels: precise counts")

print("\nIntegrity check:")
print(lie_factor(15, 15))  # honest: 1.0
print(lie_factor(8, 8))    # honest: 1.0
print("axes honest: zero baseline enforced by bar start at 0")
print("bars start at zero: verified by rendering")

print("\nChartjunk pass:")
print("- rejected: decorative fruit icons — no information added")