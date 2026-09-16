import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.orm import Worker, Cartridge, Shift, ShiftStatus, CartridgeStatus
from app.schemas import ShiftStartRequest, ShiftOut

router = APIRouter(prefix="/api/shifts", tags=["shifts"])


@router.post("/start", response_model=ShiftOut)
def start_shift(req: ShiftStartRequest, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.worker_id == req.worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    cartridge = db.query(Cartridge).filter(Cartridge.cartridge_id == req.cartridge_id).first()
    if not cartridge:
        raise HTTPException(status_code=404, detail="Cartridge not found - scan/register it first")

    if cartridge.status == CartridgeStatus.expired or cartridge.expiry_date < datetime.datetime.utcnow():
        raise HTTPException(status_code=400, detail="CARTRIDGE EXPIRED - use a fresh cartridge")

    if cartridge.status == CartridgeStatus.used:
        raise HTTPException(status_code=400, detail="Cartridge already used - insert a fresh cartridge")

    existing_active = (
        db.query(Shift)
        .filter(Shift.worker_id == worker.id, Shift.status == ShiftStatus.active)
        .first()
    )
    if existing_active:
        raise HTTPException(status_code=400, detail="Worker already has an active shift")

    shift = Shift(
        worker_id=worker.id,
        cartridge_id=cartridge.id,
        shift_label=req.shift_label or "Shift",
        status=ShiftStatus.active,
    )
    cartridge.status = CartridgeStatus.in_use
    db.add(shift)
    db.commit()
    db.refresh(shift)
    return shift


@router.post("/{shift_id}/end", response_model=ShiftOut)
def end_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    if shift.status == ShiftStatus.ended:
        return shift

    shift.status = ShiftStatus.ended
    shift.end_time = datetime.datetime.utcnow()
    if shift.cartridge:
        shift.cartridge.status = CartridgeStatus.used
    db.commit()
    db.refresh(shift)
    return shift


@router.get("/{shift_id}", response_model=ShiftOut)
def get_shift(shift_id: int, db: Session = Depends(get_db)):
    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    return shift


@router.get("/worker/{worker_id}/history", response_model=List[ShiftOut])
def worker_history(worker_id: str, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.worker_id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return (
        db.query(Shift)
        .filter(Shift.worker_id == worker.id)
        .order_by(Shift.start_time.desc())
        .all()
    )
