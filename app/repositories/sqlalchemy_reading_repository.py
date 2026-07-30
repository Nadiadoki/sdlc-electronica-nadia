from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import ReadingModel


class SQLAlchemyReadingRepository:
    """Implementacion real del repositorio, respaldada por una base de datos SQL."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(sensor_id=sensor_id, value=value, unit=unit)
        self._db.add(reading)
        self._db.commit()
        self._db.refresh(reading)
        return reading

    def get(self, reading_id: int) -> ReadingModel | None:
        return self._db.get(ReadingModel, reading_id)

    def list_for_sensor(
        self,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        from_: datetime | None = None,
        to: datetime | None = None,
    ) -> list[ReadingModel]:
        stmt = select(ReadingModel).where(
            ReadingModel.sensor_id == sensor_id, ReadingModel.active.is_(True)
        )
        if from_ is not None:
            stmt = stmt.where(ReadingModel.created_at >= from_)
        if to is not None:
            stmt = stmt.where(ReadingModel.created_at <= to)
        stmt = stmt.order_by(ReadingModel.created_at).offset(offset).limit(limit)
        return list(self._db.scalars(stmt).all())

    def update(
        self, reading_id: int, value: float | None = None, unit: str | None = None
    ) -> ReadingModel | None:
        reading = self.get(reading_id)
        if reading is None:
            return None
        if value is not None:
            reading.value = value
        if unit is not None:
            reading.unit = unit
        self._db.commit()
        self._db.refresh(reading)
        return reading

    def deactivate(self, reading_id: int) -> bool:
        reading = self.get(reading_id)
        if reading is None or not reading.active:
            return False
        reading.active = False
        self._db.commit()
        return True
