from typing import Protocol

from app.db import AlertModel


class AlertRepository(Protocol): 
    def add(self, sensor_id: str, reading_id: int, value: float, threshold: float) -> AlertModel: ... 
    def list_for_sensor(self, sensor_id: str, limit: int = 50, offset: int = 0) -> list[AlertModel]: ... 
