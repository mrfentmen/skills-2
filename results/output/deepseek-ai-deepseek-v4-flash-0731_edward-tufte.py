import math

data = {"apples": 12, "bananas": 8, "cherries": 15}
max_val = max(data.values())
scale = 1  # one '#' per unit

# Build bars starting at zero, no axes needed (labels carry the identity)
print("Chart (each # = 1 unit):")
for label, value in data.items():
    bar = "#" * value
    print(f"{label:10s} |{bar} {value}")

print("\n--- Audit ---")

# Data-ink audit
print("Data-ink audit:")
print("- Erased: all gridlines, axis lines, tick marks, borders, background, legend, title, and any 3D/shadow effects — none carried data.")
print("- Surviving marks: each '#' carries exactly 1 unit of value; each label carries the category identity; the number at the end carries the exact value for precise reading.")

# Integrity check
print("\nIntegrity check:")
print(f"- Lie factor = {1.0} (size shown equals size in data, 1:1 scale).")
print("- Bars start at zero (no truncated axis).")
print("- Axes honest: no axis exists, so no distortion possible; the visual length is directly proportional to the number.")

# Chartjunk pass
print("\nChartjunk pass:")
print("- Rejected: the decorative fruit emoji icons (🍎🍌🍒) that would have been added per row — they add noise, not information.")
print("- Rejected: a drop shadow and rounded corners on the bars — pure decoration.")

# Multiples move
print("\nMultiples move:")
print("- Three bars on the same scale, one row each — the eye scans across and sees cherries dominate, bananas lag.")

# Context line
print("\nContext line:")
print("- Compared to what? Compared to each other in the same harvest batch; the absolute values are shown, so no external baseline is needed.")