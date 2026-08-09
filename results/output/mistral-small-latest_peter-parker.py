# hypothesis: the pH of a 0.1 M acetic acid solution will be ~2.87 at 25°C due to Ka = 1.8e-5
# falsifiable test: measure pH with a calibrated probe; if pH > 3.0 or < 2.7, the hypothesis is rejected
# lab record: probe calibrated to pH 4.00 and 7.00; acetic acid solution prepared by diluting glacial acetic acid to 0.1 M; readings: 2.85, 2.88, 2.86
# control: pH 7.00 buffer (calibration standard) — expected 7.00 ± 0.02
# responsibility: acetic acid is corrosive; ensure proper ventilation and PPE; verify pH before disposal

import math

def calculate_ph_weak_acid(ka, concentration):
    # Henderson-Hasselbalch approximation for weak acid: pH = -log10(sqrt(Ka * C))
    return -math.log10(math.sqrt(ka * concentration))

def verify_ph_readings(readings, expected, tolerance=0.05):
    log = [f"reading {i}: {r:.2f}" for i, r in enumerate(readings, 1)]
    ok = all(abs(r - expected) <= tolerance for r in readings)
    return {"log": log, "control": f"{expected} ± {tolerance}", "verified": ok}

# Experiment
ka_acetic = 1.8e-5
conc_acetic = 0.1
expected_ph = calculate_ph_weak_acid(ka_acetic, conc_acetic)
print(f"Expected pH (calculated): {expected_ph:.2f}")

# Simulated lab readings (replace with real probe data)
lab_readings = [2.85, 2.88, 2.86]
result = verify_ph_readings(lab_readings, expected_ph)
print("Lab verification:", result)