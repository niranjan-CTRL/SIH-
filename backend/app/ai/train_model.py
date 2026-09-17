"""
Trains the cumulative-exposure regression model from calibration_data.csv.

Run with real data:   place a real calibration_data.csv (same columns) in
this folder, generated from the controlled lab protocol in spec section 23,
then run: python -m app.ai.train_model
"""
import warnings
warnings.filterwarnings('ignore')

import os
import json
import csv
import numpy as np
import cv2
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

HERE = os.path.dirname(__file__)
DATA_PATH = os.path.join(HERE, "calibration_data.csv")
MODEL_PATH = os.path.join(HERE, "model.joblib")
METRICS_PATH = os.path.join(HERE, "model_metrics.json")


def rgb_to_features(r, g, b, temp_c, humidity_pct, cartridge_age_days):
    """Build the same feature vector used at inference time (color_analysis.py)."""
    bgr = np.array([[[np.clip(b, 0, 255), np.clip(g, 0, 255), np.clip(r, 0, 255)]]], dtype=np.uint8)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)[0][0]
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)[0][0]

    baseline = np.array([232, 226, 210], dtype=float)
    color_dist = float(np.linalg.norm(np.array([r, g, b], dtype=float) - baseline))

    return [
        r, g, b,
        float(hsv[0]), float(hsv[1]), float(hsv[2]),
        float(lab[0]), float(lab[1]), float(lab[2]),
        color_dist,
        temp_c, humidity_pct, cartridge_age_days,
    ]


FEATURE_NAMES = [
    "r", "g", "b", "h", "s", "v", "L", "a", "bstar",
    "color_dist_from_baseline", "temp_c", "humidity_pct", "cartridge_age_days",
]


def main():
    if not os.path.exists(DATA_PATH):
        raise SystemExit(
            f"No calibration data at {DATA_PATH}. "
            "Run generate_synthetic_calibration.py first (demo only), "
            "or supply a real calibration_data.csv for production."
        )

    X, y = [], []
    with open(DATA_PATH) as f:
        for row in csv.DictReader(f):
            feats = rgb_to_features(
                float(row["r"]), float(row["g"]), float(row["b"]),
                float(row["temp_c"]), float(row["humidity_pct"]),
                float(row["cartridge_age_days"]),
            )
            X.append(feats)
            y.append(float(row["known_dose_ppm_hr"]))

    X = np.array(X)
    y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = RandomForestRegressor(n_estimators=200, max_depth=6, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    metrics = {
        "mae": float(mean_absolute_error(y_test, preds)),
        "rmse": float(mean_squared_error(y_test, preds) ** 0.5),
        "r2": float(r2_score(y_test, preds)),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "feature_names": FEATURE_NAMES,
        "trained_on": "SYNTHETIC placeholder data - not lab calibrated",
    }

    joblib.dump(model, MODEL_PATH)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print("Model trained on SYNTHETIC data (prototype only).")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
