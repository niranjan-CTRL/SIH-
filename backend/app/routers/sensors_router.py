import os
import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.orm import Shift, SensorReading, Alert, AlertType, ShiftStatus
from app.schemas import SensorReadingIn, SensorReadingOut, AlertOut

router = APIRouter(prefix="/api/sensors", tags=["sensors"])

# Configurable thresholds (spec section 12). Real deployments should tune
# these per applicable occupational safety standard for the target site.
WARNING_PPM = float(os.getenv("H2S_WARNING_PPM", "10"))
DANGER_PPM = float(os.getenv("H2S_DANGER_PPM", "20"))
EMERGENCY_PPM = float(os.getenv("H2S_EMERGENCY_PPM", "50"))


def _check_thresholds(db: Session, shift: Shift, reading: SensorReading):
    if reading.h2s_ppm > shift.peak_h2s_ppm:
        shift.peak_h2s_ppm = reading.h2s_ppm

    if reading.h2s_ppm >= EMERGENCY_PPM:
        db.add(Alert(
            shift_id=shift.id, worker_id=shift.worker_id, type=AlertType.emergency,
            message=f"EMERGENCY: H2S reading {reading.h2s_ppm} ppm exceeds emergency threshold ({EMERGENCY_PPM} ppm)",
        ))
    elif reading.h2s_ppm >= DANGER_PPM:
        shift.danger_count += 1
        db.add(Alert(
            shift_id=shift.id, worker_id=shift.worker_id, type=AlertType.danger,
            message=f"DANGER: H2S reading {reading.h2s_ppm} ppm exceeds danger threshold ({DANGER_PPM} ppm)",
        ))
    elif reading.h2s_ppm >= WARNING_PPM:
        shift.warning_count += 1
        db.add(Alert(
            shift_id=shift.id, worker_id=shift.worker_id, type=AlertType.warning,
            message=f"Warning: H2S reading {reading.h2s_ppm} ppm exceeds warning threshold ({WARNING_PPM} ppm)",
        ))

    if reading.motion_state == "fall_suspected":
        db.add(Alert(
            shift_id=shift.id, worker_id=shift.worker_id, type=AlertType.fall,
            message="Possible fall detected - countdown triggered, confirm worker status",
        ))
    elif reading.motion_state == "inactive":
        db.add(Alert(
            shift_id=shift.id, worker_id=shift.worker_id, type=AlertType.inactivity,
            message="Prolonged inactivity detected",
        ))


@router.post("/{shift_id}/reading", response_model=SensorReadingOut)
def add_reading(shift_id: int, reading_in: SensorReadingIn, db: Session = Depends(get_db)):
    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    if shift.status != ShiftStatus.active:
        raise HTTPException(status_code=400, detail="Shift is not active")

    last_reading = db.query(SensorReading).filter(SensorReading.shift_id == shift_id).order_by(SensorReading.timestamp.desc()).first()

    reading = SensorReading(shift_id=shift_id, **reading_in.model_dump())
    reading.timestamp = datetime.datetime.utcnow()
    db.add(reading)

    if last_reading:
        time_diff_hours = (reading.timestamp - last_reading.timestamp).total_seconds() / 3600.0
        shift.cumulative_exposure_ppm_hr += ((last_reading.h2s_ppm + reading.h2s_ppm) / 2.0) * time_diff_hours

    db.flush()  # get reading in session before threshold check uses it

    _check_thresholds(db, shift, reading)

    db.commit()
    db.refresh(reading)
    
    reading_out = SensorReadingOut.model_validate(reading)
    reading_out.cumulative_exposure_ppm_hr = shift.cumulative_exposure_ppm_hr
    return reading_out


@router.get("/{shift_id}/latest", response_model=SensorReadingOut)
def latest_reading(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    reading = (
        db.query(SensorReading)
        .filter(SensorReading.shift_id == shift_id)
        .order_by(SensorReading.timestamp.desc())
        .first()
    )
    if not reading:
        raise HTTPException(status_code=404, detail="No readings yet for this shift")
        
    reading_out = SensorReadingOut.model_validate(reading)
    if shift:
        reading_out.cumulative_exposure_ppm_hr = shift.cumulative_exposure_ppm_hr
    return reading_out


@router.get("/{shift_id}/history", response_model=List[SensorReadingOut])
def reading_history(shift_id: int, limit: int = 100, db: Session = Depends(get_db)):
    return (
        db.query(SensorReading)
        .filter(SensorReading.shift_id == shift_id)
        .order_by(SensorReading.timestamp.desc())
        .limit(limit)
        .all()
    )


@router.get("/{shift_id}/alerts", response_model=List[AlertOut])
def shift_alerts(shift_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Alert)
        .filter(Alert.shift_id == shift_id)
        .order_by(Alert.timestamp.desc())
        .all()
    )
