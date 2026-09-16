"""
Cartridge photo -> estimated cumulative exposure.

Pipeline (spec section 9 / 24):
  camera image -> strip region crop -> reference-patch lighting correction
  -> RGB/HSV/Lab feature extraction -> calibration model -> dose estimate

NOTE on the reference scale (spec section 6/24): a production cartridge
has a printed reference color scale next to the sensing strip so the app
can normalize for lighting. This prototype expects the guided scan box to
place the strip in the CENTER of the frame and a neutral/white reference
patch in the TOP-LEFT corner of the frame (as instructed in the mobile
scan UI). Swap `_locate_regions` for real strip/marker detection (e.g.
ArUco markers or a printed QR frame) once the physical cartridge design
is finalized.
"""
import os
import json
import numpy as np
import cv2
import joblib

HERE = os.path.dirname(__file__)
MODEL_PATH = os.path.join(HERE, "model.joblib")
METRICS_PATH = os.path.join(HERE, "model_metrics.json")

_model = None
_metrics = None


def _load_model():
    global _model, _metrics
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(
                "No trained model found. Run `python -m app.ai.train_model` first."
            )
        _model = joblib.load(MODEL_PATH)
        with open(METRICS_PATH) as f:
            _metrics = json.load(f)
    return _model, _metrics


def _locate_regions(img_bgr: np.ndarray):
    """Return (strip_roi, reference_roi) as image crops.

    Simplified for the prototype: center square = strip, top-left square =
    reference patch, per the guided scan-box UI on the frontend.
    """
    h, w = img_bgr.shape[:2]
    side = int(min(h, w) * 0.28)

    cy, cx = h // 2, w // 2
    strip = img_bgr[cy - side // 2: cy + side // 2, cx - side // 2: cx + side // 2]

    ref_side = int(min(h, w) * 0.14)
    margin = int(min(h, w) * 0.04)
    reference = img_bgr[margin: margin + ref_side, margin: margin + ref_side]

    return strip, reference


def _mean_bgr(crop: np.ndarray):
    if crop.size == 0:
        raise ValueError("Empty crop region - image may be too small or malformed.")
    b, g, r = cv2.mean(crop)[:3]
    return r, g, b


def _lighting_correct(strip_rgb, reference_rgb, assumed_reference_rgb=(230, 230, 230)):
    """Scale the strip color by how far the reference patch is from its
    known/expected neutral value, per-channel. This is a simplified gray-world
    correction; a real reference scale (multiple known swatches) would give a
    stronger correction via linear regression per channel."""
    r, g, b = strip_rgb
    rr, rg, rb = reference_rgb
    ar, ag, ab = assumed_reference_rgb

    def safe_ratio(a, b_):
        return a / b_ if b_ > 1e-6 else 1.0

    r_corr = min(255.0, r * safe_ratio(ar, rr))
    g_corr = min(255.0, g * safe_ratio(ag, rg))
    b_corr = min(255.0, b * safe_ratio(ab, rb))
    return r_corr, g_corr, b_corr


def _quality_check(reference_rgb):
    """Reject scans where the reference patch itself is implausible (too
    dark = poor lighting/covered; near-uniform extreme values = blown out)."""
    r, g, b = reference_rgb
    brightness = (r + g + b) / 3
    if brightness < 25:
        return False, "Image too dark - retake in better lighting with the reference patch visible."
    if brightness > 250:
        return False, "Image overexposed - avoid direct flash glare on the reference patch."
    return True, None


def analyze_cartridge_image(image_bytes: bytes, temp_c: float = 28.0,
                             humidity_pct: float = 55.0,
                             cartridge_age_days: float = 1.0):
    """Full pipeline. Returns a dict with features, estimate, and disclaimers."""
    model, metrics = _load_model()

    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image - upload a JPEG or PNG photo.")

    strip_roi, reference_roi = _locate_regions(img)
    strip_rgb = _mean_bgr(strip_roi)
    reference_rgb = _mean_bgr(reference_roi)

    ok, reason = _quality_check(reference_rgb)

    corrected_rgb = _lighting_correct(strip_rgb, reference_rgb)
    r, g, b = corrected_rgb

    bgr_pixel = np.uint8([[[b, g, r]]])
    hsv = cv2.cvtColor(bgr_pixel, cv2.COLOR_BGR2HSV)[0][0]
    lab = cv2.cvtColor(bgr_pixel, cv2.COLOR_BGR2LAB)[0][0]

    baseline = np.array([232, 226, 210], dtype=float)
    color_dist = float(np.linalg.norm(np.array([r, g, b]) - baseline))

    features = [
        r, g, b,
        float(hsv[0]), float(hsv[1]), float(hsv[2]),
        float(lab[0]), float(lab[1]), float(lab[2]),
        color_dist, temp_c, humidity_pct, cartridge_age_days,
    ]

    dose_estimate = float(model.predict([features])[0])
    dose_estimate = max(0.0, dose_estimate)

    if dose_estimate < 10:
        risk = "LOW"
    elif dose_estimate < 30:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {
        "ok": ok,
        "quality_warning": reason,
        "strip_rgb": {"r": round(r, 1), "g": round(g, 1), "b": round(b, 1)},
        "hsv": {"h": float(hsv[0]), "s": float(hsv[1]), "v": float(hsv[2])},
        "lab": {"L": float(lab[0]), "a": float(lab[1]), "b": float(lab[2])},
        "color_distance_from_baseline": round(color_dist, 2),
        "estimated_cumulative_exposure_ppm_hr": round(dose_estimate, 2),
        "risk_level": risk,
        "model_version": "placeholder-v0",
        "is_validated_model": False,
        "model_metrics": metrics,
        "disclaimer": (
            "This estimate comes from a model trained on SYNTHETIC calibration "
            "data for prototype/demo purposes only. It has NOT been validated "
            "against real controlled H2S exposures and must not be used for "
            "real safety decisions until the lab calibration in the project "
            "spec (section 23/29) is completed."
        ),
    }
