from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.orm import Worker
from app.schemas import LoginRequest, LoginResponse
from app.auth import verify_pin, create_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.worker_id == req.worker_id).first()
    if not worker or not verify_pin(req.pin, worker.pin_hash):
        raise HTTPException(status_code=401, detail="Invalid worker ID or PIN")

    token = create_token(worker.worker_id, worker.role)
    return LoginResponse(
        token=token, worker_id=worker.worker_id, name=worker.name, role=worker.role
    )
