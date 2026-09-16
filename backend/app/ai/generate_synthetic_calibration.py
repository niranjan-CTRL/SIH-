"""
IMPORTANT - READ BEFORE USING IN PRODUCTION
============================================
This script generates a SYNTHETIC calibration dataset. It does NOT contain
real experimental data from controlled H2S gas exposure of actual chemical
cartridges. It exists only so the prototype has an end-to-end, runnable
AI pipeline to demonstrate the architecture described in the project spec
(section 23: "AI Development and Calibration").

Per the project spec: "Actual values MUST come from controlled experiments;
never invent results." The model trained on this data is NOT validated and
must NEVER be presented to a real worker as giving a real exposure reading.
Every prediction made with it is labeled `is_validated_model = False` and
`model_version = "placeholder-v0"` throughout the app.

To go from prototype -> real product:
1. Run the actual calibration protocol in section 23/29 of the spec
   (controlled concentrations x durations, photograph each cartridge under
   the same lighting rig, record known dose).
2. Replace this file's output (calibration_data.csv) with the real dataset.
3. Re-run train_model.py. It doesn't need any other code changes.
"""
import csv
import os
import random

random.seed(42)

OUT_PATH = os.path.join(os.path.dirname(__file__), "calibration_data.csv")

# Simulated chemistry: an unexposed strip is near-white/cream. As cumulative
# dose (ppm*hr) rises, the strip darkens and shifts toward brown, roughly
# following a saturating exponential (mimics typical colorimetric dosimeter
# behavior) plus per-sample noise and lighting jitter.
BASELINE_RGB = (232, 226, 210)
DARK_RGB = (58, 40, 28)


def darken(dose_ppm_hr: float):
    # saturating response curve, dose in [0, 60] ppm*hr mapped to [0,1]
    k = 0.055
    t = 1 - pow(2.71828, -k * dose_ppm_hr)
    r = BASELINE_RGB[0] + (DARK_RGB[0] - BASELINE_RGB[0]) * t
    g = BASELINE_RGB[1] + (DARK_RGB[1] - BASELINE_RGB[1]) * t
    b = BASELINE_RGB[2] + (DARK_RGB[2] - BASELINE_RGB[2]) * t
    return r, g, b


def add_noise(v, scale=4.0):
    return max(0, min(255, v + random.gauss(0, scale)))


rows = []
concentrations = [1, 2, 5, 8, 10, 15, 20, 25]
durations = [0.5, 1, 2, 3, 4, 6, 8]

for c in concentrations:
    for h in durations:
        dose = c * h
        for _replicate in range(3):
            # small lighting jitter simulates imperfect lighting correction
            lighting_jitter = random.gauss(1.0, 0.03)
            r, g, b = darken(dose)
            r = add_noise(r * lighting_jitter)
            g = add_noise(g * lighting_jitter)
            b = add_noise(b * lighting_jitter)
            temp_c = round(random.uniform(22, 38), 1)
            humidity_pct = round(random.uniform(30, 85), 1)
            cartridge_age_days = random.randint(0, 25)
            rows.append({
                "concentration_ppm": c,
                "duration_hr": h,
                "known_dose_ppm_hr": dose,
                "r": round(r, 2),
                "g": round(g, 2),
                "b": round(b, 2),
                "temp_c": temp_c,
                "humidity_pct": humidity_pct,
                "cartridge_age_days": cartridge_age_days,
            })

with open(OUT_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} SYNTHETIC calibration rows to {OUT_PATH}")
