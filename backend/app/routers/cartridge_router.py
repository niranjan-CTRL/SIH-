import datetime
import json
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.orm import Cartridge, CartridgeStatus, Shift, ExposureRecord

router = APIRouter(prefix="/api/cartridge", tags=["cartridge"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

DEFAULT_SHELF_LIFE_DAYS = int(os.getenv("CARTRIDGE_SHELF_LIFE_DAYS", "30"))


@router.post("/register")
def register_cartridge(cartridge_id: str = Form(...), db: Session = Depends(get_db)):
    existing = db.query(Cartridge).filter(Cartridge.cartridge_id == cartridge_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Cartridge ID already registered")

    cartridge = Cartridge(
        cartridge_id=cartridge_id,
        expiry_date=datetime.datetime.utcnow() + datetime.timedelta(days=DEFAULT_SHELF_LIFE_DAYS),
        status=CartridgeStatus.new,
    )
    db.add(cartridge)
    db.commit()
    db.refresh(cartridge)
    return {
        "cartridge_id": cartridge.cartridge_id,
        "status": cartridge.status,
        "expiry_date": cartridge.expiry_date,
        "note": (
            f"Shelf life set to {DEFAULT_SHELF_LIFE_DAYS} days as a PLACEHOLDER "
            "default for the prototype - spec section 25 requires this to come "
            "from validated experimental shelf-life testing, not an assumption."
        ),
    }


@router.get("/{cartridge_id}")
def get_cartridge(cartridge_id: str, db: Session = Depends(get_db)):
    cartridge = db.query(Cartridge).filter(Cartridge.cartridge_id == cartridge_id).first()
    if not cartridge:
        raise HTTPException(status_code=404, detail="Cartridge not found")

    is_expired = cartridge.expiry_date < datetime.datetime.utcnow()
    if is_expired and cartridge.status != CartridgeStatus.expired:
        cartridge.status = CartridgeStatus.expired
        db.commit()

    return {
        "cartridge_id": cartridge.cartridge_id,
        "status": cartridge.status,
        "issued_date": cartridge.issued_date,
        "expiry_date": cartridge.expiry_date,
        "is_expired": is_expired,
    }


@router.post("/scan")
async def scan_cartridge(
    shift_id: int = Form(...),
    cartridge_id: str = Form(...),
    temp_c: float = Form(28.0),
    humidity_pct: float = Form(55.0),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    cartridge = db.query(Cartridge).filter(Cartridge.cartridge_id == cartridge_id).first()
    if not cartridge:
        raise HTTPException(status_code=404, detail="Cartridge not registered")
    if cartridge.expiry_date < datetime.datetime.utcnow():
        raise HTTPException(status_code=400, detail="CARTRIDGE EXPIRED - dose estimation blocked")

    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image upload")

    cartridge_age_days = (datetime.datetime.utcnow() - cartridge.issued_date).days

    try:
        # Lazy import to avoid Windows numpy/joblib initialization issues
        from app.ai.color_analysis import analyze_cartridge_image
        result = analyze_cartridge_image(
            image_bytes, temp_c=temp_c, humidity_pct=humidity_pct,
            cartridge_age_days=cartridge_age_days,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(image_bytes)

    record = ExposureRecord(
        shift_id=shift_id,
        cartridge_id=cartridge_id,
        image_path=filepath,
        features_json=json.dumps({
            "strip_rgb": result["strip_rgb"],
            "hsv": result["hsv"],
            "lab": result["lab"],
            "color_distance_from_baseline": result["color_distance_from_baseline"],
        }),
        estimated_dose_ppm_hr=result["estimated_cumulative_exposure_ppm_hr"],
        model_version=result["model_version"],
        is_validated_model=result["is_validated_model"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {"record_id": record.id, **result}
