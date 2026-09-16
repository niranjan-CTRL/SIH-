import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    worker_id: str
    pin: str


class LoginResponse(BaseModel):
    token: str
    worker_id: str
    name: str
    role: str


class ShiftStartRequest(BaseModel):
    worker_id: str
    cartridge_id: str
    shift_label: Optional[str] = "Shift"


class ShiftOut(BaseModel):
    id: int
    worker_id: int
    shift_label: str
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime]
    status: str
    peak_h2s_ppm: float
    warning_count: int
    danger_count: int

    class Config:
        from_attributes = True


class SensorReadingIn(BaseModel):
    h2s_ppm: float
    hr_bpm: Optional[float] = None
    spo2_pct: Optional[float] = None
    temp_c: Optional[float] = None
    motion_state: Optional[str] = "normal"


class SensorReadingOut(SensorReadingIn):
    id: int
    shift_id: int
    timestamp: datetime.datetime
    cumulative_exposure_ppm_hr: Optional[float] = None

    class Config:
        from_attributes = True


class SOSRequest(BaseModel):
    shift_id: int


class ExposureRecordOut(BaseModel):
    model_config = ConfigDict(protected_namespaces=(), from_attributes=True)

    id: int
    shift_id: int
    cartridge_id: str
    estimated_dose_ppm_hr: float
    model_version: str
    is_validated_model: bool
    created_at: datetime.datetime


class AlertOut(BaseModel):
    id: int
    shift_id: int
    worker_id: int
    type: str
    message: str
    timestamp: datetime.datetime
    acknowledged: bool

    class Config:
        from_attributes = True


class WorkerStatusOut(BaseModel):
    worker_id: str
    name: str
    shift_id: Optional[int]
    shift_status: Optional[str]
    latest_h2s_ppm: Optional[float]
    latest_hr_bpm: Optional[float]
    latest_spo2_pct: Optional[float]
    latest_temp_c: Optional[float]
    risk_level: str
    open_alerts: int
