import datetime
from app.database import SessionLocal
from app.models.orm import Worker, Cartridge, CartridgeStatus
from app.auth import hash_pin


def seed_demo_data():
    db = SessionLocal()
    try:
        if db.query(Worker).count() == 0:
            db.add_all([
                Worker(worker_id="W101", name="Arjun Rao", pin_hash=hash_pin("1234"), role="worker"),
                Worker(worker_id="W102", name="Priya Nair", pin_hash=hash_pin("1234"), role="worker"),
                Worker(worker_id="S001", name="Supervisor Menon", pin_hash=hash_pin("9999"), role="supervisor"),
            ])
        if db.query(Cartridge).count() == 0:
            db.add_all([
                Cartridge(
                    cartridge_id="H2S-CART-001",
                    expiry_date=datetime.datetime.utcnow() + datetime.timedelta(days=30),
                    status=CartridgeStatus.new,
                ),
                Cartridge(
                    cartridge_id="H2S-CART-002",
                    expiry_date=datetime.datetime.utcnow() + datetime.timedelta(days=30),
                    status=CartridgeStatus.new,
                ),
            ])
        db.commit()
    finally:
        db.close()
