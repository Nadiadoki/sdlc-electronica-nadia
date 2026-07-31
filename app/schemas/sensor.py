from datetime import datetime
from typing import Literal

from pydantic import BaseModel

SensorTypeLiteral = Literal["temperature", "humidity"]


class SensorCreate(BaseModel):
    sensor_id: str
    sensor_type: SensorTypeLiteral


class SensorUpdate(BaseModel):
    sensor_type: SensorTypeLiteral | None = None


class SensorOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    sensor_id: str
    sensor_type: str
    active: bool
    created_at: datetime
