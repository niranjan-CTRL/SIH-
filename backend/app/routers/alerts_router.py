from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.orm import Shift, Alert, AlertType
from app.schemas import SOSRequest, AlertOut

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.post("/sos", response_model=AlertOut)
def trigger_sos(req: SOSRequest, db: Session = Depends(get_db)):
    shift = db.query(Shift).filter(Shift.id == req.shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    alert = Alert(
        shift_id=shift.id,
        worker_id=shift.worker_id,
        type=AlertType.sos,
        message="SOS button pressed - immediate emergency response needed",
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


@router.post("/{alert_id}/acknowledge", response_model=AlertOut)
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.acknowledged = True
    db.commit()
    db.refresh(alert)
    return alert
