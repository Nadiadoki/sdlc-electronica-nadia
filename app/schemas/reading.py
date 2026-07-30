from datetime import datetime

from pydantic import BaseModel


class ReadingCreate(BaseModel):
    value: float
    unit: str = "C"


class ReadingUpdate(BaseModel):
    value: float | None = None
    unit: str | None = None


class ReadingOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    sensor_id: str
    value: float
    unit: str
    created_at: datetime
    active: bool
