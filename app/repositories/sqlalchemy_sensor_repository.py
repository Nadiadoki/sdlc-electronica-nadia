from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SensorModel


class SQLAlchemySensorRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def add(self, sensor_id: str, sensor_type: str) -> SensorModel:
        sensor = SensorModel(sensor_id=sensor_id, sensor_type=sensor_type)
        self._db.add(sensor)
        self._db.commit()
        self._db.refresh(sensor)
        return sensor

    def get_by_sensor_id(self, sensor_id: str) -> SensorModel | None:
        stmt = select(SensorModel).where(SensorModel.sensor_id == sensor_id)
        return self._db.scalars(stmt).first()

    def list(self, limit: int = 50, offset: int = 0) -> list[SensorModel]:
        stmt = (
            select(SensorModel)
            .where(SensorModel.active.is_(True))
            .order_by(SensorModel.created_at)
            .offset(offset)
            .limit(limit)
        )
        return list(self._db.scalars(stmt).all())

    def update(self, sensor_id: str, sensor_type: str | None = None) -> SensorModel | None:
        sensor = self.get_by_sensor_id(sensor_id)
        if sensor is None:
            return None
        if sensor_type is not None:
            sensor.sensor_type = sensor_type
        self._db.commit()
        self._db.refresh(sensor)
        return sensor

    def deactivate(self, sensor_id: str) -> bool:
        sensor = self.get_by_sensor_id(sensor_id)
        if sensor is None or not sensor.active:
            return False
        sensor.active = False
        self._db.commit()
        return True
