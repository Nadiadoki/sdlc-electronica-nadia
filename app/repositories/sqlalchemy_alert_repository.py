from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import AlertModel


class SQLAlchemyAlertRepository: 
    def __init__(self, db: Session) -> None: 
        self._db = db 
    def add(self, sensor_id: str, reading_id: int, value: float, threshold: float) -> AlertModel: 
        alert = AlertModel(sensor_id=sensor_id, reading_id=reading_id, value=value, threshold=threshold) 
        self._db.add(alert) 
        self._db.commit() 
        self._db.refresh(alert) 
        return alert 
    def list_for_sensor(self, sensor_id: str, limit: int = 50, offset: int = 0) -> list[AlertModel]: 
        safe_limit = max(1, min(limit, 500)) 
        safe_offset = max(0, offset) 
        stmt = ( 
            select(AlertModel) 
            .where(AlertModel.sensor_id == sensor_id) 
            .order_by(AlertModel.created_at) 
            .offset(safe_offset) 
            .limit(safe_limit) 
        ) 
        return list(self._db.scalars(stmt).all()) 
