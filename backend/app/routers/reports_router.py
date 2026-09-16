from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.orm import Shift, ExposureRecord, Alert, SensorReading

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/{shift_id}")
def shift_report(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    exposure_records = (
        db.query(ExposureRecord)
        .filter(ExposureRecord.shift_id == shift_id)
        .order_by(ExposureRecord.created_at.desc())
        .all()
    )
    alerts = db.query(Alert).filter(Alert.shift_id == shift_id).all()

    avg_h2s = db.query(func.avg(SensorReading.h2s_ppm)).filter(SensorReading.shift_id == shift_id).scalar() or 0.0
    avg_hr = db.query(func.avg(SensorReading.hr_bpm)).filter(SensorReading.shift_id == shift_id).scalar()
    avg_spo2 = db.query(func.avg(SensorReading.spo2_pct)).filter(SensorReading.shift_id == shift_id).scalar()
    avg_temp = db.query(func.avg(SensorReading.temp_c)).filter(SensorReading.shift_id == shift_id).scalar()

    latest_exposure = exposure_records[0] if exposure_records else None
    status = "NORMAL"
    if shift.danger_count > 0 or (latest_exposure and latest_exposure.estimated_dose_ppm_hr >= 30):
        status = "REVIEW REQUIRED"
    elif shift.warning_count > 0:
        status = "MONITOR"

    return {
        "worker": shift.worker.worker_id,
        "worker_name": shift.worker.name,
        "shift_label": shift.shift_label,
        "start_time": shift.start_time,
        "end_time": shift.end_time,
        "peak_h2s_ppm": shift.peak_h2s_ppm,
        "avg_h2s_ppm": avg_h2s,
        "avg_hr_bpm": avg_hr,
        "avg_spo2_pct": avg_spo2,
        "avg_temp_c": avg_temp,
        "warning_count": shift.warning_count,
        "danger_count": shift.danger_count,
        "cartridge_id": shift.cartridge.cartridge_id if shift.cartridge else None,
        "estimated_cumulative_exposure_ppm_hr": shift.cumulative_exposure_ppm_hr,
        "exposure_model_validated": (
            latest_exposure.is_validated_model if latest_exposure else None
        ),
        "status": status,
        "sos_events": len([a for a in alerts if a.type == "sos"]),
        "fall_events": len([a for a in alerts if a.type == "fall"]),
        "total_alerts": len(alerts),
    }
