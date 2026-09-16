from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.orm import Worker, Shift, SensorReading, Alert, ShiftStatus
from app.schemas import WorkerStatusOut, AlertOut
from app.routers.sensors_router import WARNING_PPM, DANGER_PPM, EMERGENCY_PPM

router = APIRouter(prefix="/api/supervisor", tags=["supervisor"])


def _risk_level(h2s_ppm):
    if h2s_ppm is None:
        return "UNKNOWN"
    if h2s_ppm >= EMERGENCY_PPM:
        return "EMERGENCY"
    if h2s_ppm >= DANGER_PPM:
        return "DANGER"
    if h2s_ppm >= WARNING_PPM:
        return "WARNING"
    return "NORMAL"


@router.get("/workers", response_model=List[WorkerStatusOut])
def worker_board(db: Session = Depends(get_db)):
    workers = db.query(Worker).filter(Worker.role == "worker").all()
    out = []
    for w in workers:
        shift = (
            db.query(Shift)
            .filter(Shift.worker_id == w.id, Shift.status == ShiftStatus.active)
            .first()
        )
        latest = None
        open_alerts = 0
        if shift:
            latest = (
                db.query(SensorReading)
                .filter(SensorReading.shift_id == shift.id)
                .order_by(SensorReading.timestamp.desc())
                .first()
            )
            open_alerts = (
                db.query(Alert)
                .filter(Alert.shift_id == shift.id, Alert.acknowledged == False)  # noqa: E712
                .count()
            )

        out.append(WorkerStatusOut(
            worker_id=w.worker_id,
            name=w.name,
            shift_id=shift.id if shift else None,
            shift_status=shift.status if shift else None,
            latest_h2s_ppm=latest.h2s_ppm if latest else None,
            latest_hr_bpm=latest.hr_bpm if latest else None,
            latest_spo2_pct=latest.spo2_pct if latest else None,
            latest_temp_c=latest.temp_c if latest else None,
            risk_level=_risk_level(latest.h2s_ppm if latest else None),
            open_alerts=open_alerts,
        ))
    return out


@router.get("/alerts", response_model=List[AlertOut])
def all_open_alerts(db: Session = Depends(get_db)):
    return (
        db.query(Alert)
        .filter(Alert.acknowledged == False)  # noqa: E712
        .order_by(Alert.timestamp.desc())
        .all()
    )
