from datetime import datetime

from pydantic import BaseModel


class AlertOut(BaseModel): 
    model_config = {"from_attributes": True} 
    id: int 
    sensor_id: str 
    reading_id: int 
    value: float 
    threshold: float 
    created_at: datetime 
