import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.models import orm  # noqa: F401 ensures models are registered
from app.routers import (
    auth_router, shifts_router, sensors_router, cartridge_router,
    alerts_router, supervisor_router, reports_router,
)
from app.seed import seed_demo_data

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="H2S Sentinel API",
    description="Backend for the H2S Sentinel worker-safety prototype (Team Valence, SIH26118).",
    version="0.1.0",
)

FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
allowed_origins = [FRONTEND_URL] if FRONTEND_URL != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(auth_router.router)
app.include_router(shifts_router.router)
app.include_router(sensors_router.router)
app.include_router(cartridge_router.router)
app.include_router(alerts_router.router)
app.include_router(supervisor_router.router)
app.include_router(reports_router.router)


@app.on_event("startup")
def on_startup():
    try:
        seed_demo_data()
    except Exception as e:
        print(f"Warning: Could not seed demo data: {e}")



@app.get("/api/health")
def health():
    return {"status": "ok", "service": "h2s-sentinel-backend"}


@app.get("/")
def root():
    return {"message": "H2S Sentinel API - see /docs for endpoints"}
