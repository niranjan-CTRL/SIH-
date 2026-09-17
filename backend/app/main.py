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

# Parse FRONTEND_URL environment variable for CORS (supports comma-separated URLs or '*')
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
if FRONTEND_URL.strip() == "*":
    allowed_origins = ["*"]
else:
    allowed_origins = [url.strip() for url in FRONTEND_URL.split(",") if url.strip()]
    if "http://localhost:5173" not in allowed_origins:
        allowed_origins.append("http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
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
    # 1. Seed demo database
    try:
        seed_demo_data()
    except Exception as e:
        print(f"Warning: Could not seed demo data: {e}")

    # 2. Ensure AI model exists (critical for cloud deploys like Render where model.joblib isn't in git)
    ai_dir = os.path.join(os.path.dirname(__file__), "ai")
    model_path = os.path.join(ai_dir, "model.joblib")
    if not os.path.exists(model_path):
        print("No trained model found. Generating synthetic calibration data and training model...")
        try:
            from app.ai import generate_synthetic_calibration, train_model
            generate_synthetic_calibration.main()
            train_model.main()
            print("Model successfully generated and trained on startup.")
        except Exception as e:
            print(f"Warning: Model initialization failed: {e}")



@app.get("/api/health")
def health():
    return {"status": "ok", "service": "h2s-sentinel-backend"}


@app.get("/")
def root():
    return {"message": "H2S Sentinel API - see /docs for endpoints"}
