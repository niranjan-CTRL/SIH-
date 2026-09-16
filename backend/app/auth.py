import os
import datetime
import bcrypt
from jose import jwt, JWTError
from fastapi import HTTPException, Header

SECRET_KEY = os.getenv("JWT_SECRET", "dev-only-insecure-secret-change-me")
ALGORITHM = "HS256"
EXPIRE_HOURS = 12


def hash_pin(pin: str) -> str:
    return bcrypt.hashpw(pin.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_pin(pin: str, pin_hash: str) -> bool:
    return bcrypt.checkpw(pin.encode("utf-8"), pin_hash.encode("utf-8"))


def create_token(worker_id: str, role: str) -> str:
    payload = {
        "sub": worker_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=EXPIRE_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def get_current_claims(authorization: str = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    return decode_token(token)
