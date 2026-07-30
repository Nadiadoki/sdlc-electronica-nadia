from datetime import datetime
from typing import Protocol

from app.db import ReadingModel


class ReadingRepository(Protocol):
    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel: ...
    def get(self, reading_id: int) -> ReadingModel | None: ...
    def list_for_sensor(
        self,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        from_: datetime | None = None,
        to: datetime | None = None,
    ) -> list[ReadingModel]: ...
    def update(
        self, reading_id: int, value: float | None = None, unit: str | None = None
    ) -> ReadingModel | None: ...
    def deactivate(self, reading_id: int) -> bool: ...
