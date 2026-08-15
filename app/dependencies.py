from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.repositories.alert_repository import AlertRepository
from app.repositories.reading_repository import ReadingRepository
from app.repositories.sensor_repository import SensorRepository
from app.repositories.sqlalchemy_alert_repository import SQLAlchemyAlertRepository
from app.repositories.sqlalchemy_reading_repository import SQLAlchemyReadingRepository
from app.repositories.sqlalchemy_sensor_repository import SQLAlchemySensorRepository
from app.services.reading_service import ReadingService
from app.services.sensor_service import SensorService


def get_db() -> Generator[Session, None, None]: 
    db = SessionLocal() 
    try: 
        yield db 
    finally: 
        db.close() 
def get_reading_repository(db: Annotated[Session, Depends(get_db)]) -> ReadingRepository: 
    return SQLAlchemyReadingRepository(db) 
def get_sensor_repository(db: Annotated[Session, Depends(get_db)]) -> SensorRepository: 
    return SQLAlchemySensorRepository(db) 
def get_alert_repository(db: Annotated[Session, Depends(get_db)]) -> AlertRepository: 
    return SQLAlchemyAlertRepository(db) 
def get_sensor_service( 
    repo: Annotated[SensorRepository, Depends(get_sensor_repository)], 
) -> SensorService: 
    return SensorService(repo=repo) 
def get_reading_service( 
    reading_repo: Annotated[ReadingRepository, Depends(get_reading_repository)], 
    sensor_repo: Annotated[SensorRepository, Depends(get_sensor_repository)], 
    alert_repo: Annotated[AlertRepository, Depends(get_alert_repository)], 
) -> ReadingService: 
    return ReadingService(repo=reading_repo, sensor_repo=sensor_repo, alert_repo=alert_repo) 
