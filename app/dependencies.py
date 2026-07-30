from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.repositories.reading_repository import ReadingRepository
from app.repositories.sqlalchemy_reading_repository import SQLAlchemyReadingRepository
from app.services.reading_service import ReadingService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_reading_repository(db: Annotated[Session, Depends(get_db)]) -> ReadingRepository:
    return SQLAlchemyReadingRepository(db)


def get_reading_service(
    repo: Annotated[ReadingRepository, Depends(get_reading_repository)],
) -> ReadingService:
    return ReadingService(repo=repo)
