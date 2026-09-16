import datetime
import enum
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean, Text
)
from sqlalchemy.orm import relationship
from app.database import Base


class ShiftStatus(str, enum.Enum):
    active = "active"
    ended = "ended"


class CartridgeStatus(str, enum.Enum):
    new = "new"
    in_use = "in_use"
    used = "used"
    expired = "expired"


class AlertType(str, enum.Enum):
    warning = "warning"
    danger = "danger"
    emergency = "emergency"
    sos = "sos"
    fall = "fall"
    inactivity = "inactivity"


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    pin_hash = Column(String, nullable=False)
    role = Column(String, default="worker")  # worker | supervisor
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    shifts = relationship("Shift", back_populates="worker")


class Cartridge(Base):
    __tablename__ = "cartridges"

    id = Column(Integer, primary_key=True, index=True)
    cartridge_id = Column(String, unique=True, index=True, nullable=False)
    issued_date = Column(DateTime, default=datetime.datetime.utcnow)
    expiry_date = Column(DateTime, nullable=False)
    status = Column(Enum(CartridgeStatus), default=CartridgeStatus.new)

    shifts = relationship("Shift", back_populates="cartridge")


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    cartridge_id = Column(Integer, ForeignKey("cartridges.id"), nullable=True)
    shift_label = Column(String, default="Shift")
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(Enum(ShiftStatus), default=ShiftStatus.active)
    peak_h2s_ppm = Column(Float, default=0.0)
    warning_count = Column(Integer, default=0)
    danger_count = Column(Integer, default=0)
    cumulative_exposure_ppm_hr = Column(Float, default=0.0)

    worker = relationship("Worker", back_populates="shifts")
    cartridge = relationship("Cartridge", back_populates="shifts")
    readings = relationship("SensorReading", back_populates="shift")
    exposure_records = relationship("ExposureRecord", back_populates="shift")
    alerts = relationship("Alert", back_populates="shift")


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    h2s_ppm = Column(Float, nullable=False)
    hr_bpm = Column(Float, nullable=True)
    spo2_pct = Column(Float, nullable=True)
    temp_c = Column(Float, nullable=True)
    motion_state = Column(String, default="normal")  # normal | fall_suspected | inactive

    shift = relationship("Shift", back_populates="readings")


class ExposureRecord(Base):
    __tablename__ = "exposure_records"

    id = Column(Integer, primary_key=True, index=True)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    cartridge_id = Column(String, nullable=False)
    image_path = Column(String, nullable=True)
    features_json = Column(Text, nullable=True)
    estimated_dose_ppm_hr = Column(Float, nullable=False)
    model_version = Column(String, default="placeholder-v0")
    is_validated_model = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    shift = relationship("Shift", back_populates="exposure_records")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    type = Column(Enum(AlertType), nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    acknowledged = Column(Boolean, default=False)

    shift = relationship("Shift", back_populates="alerts")
