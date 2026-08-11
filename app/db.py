import os
from datetime import UTC, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


def get_database_url() -> str:
    url = os.getenv("DATABASE_URL", "sqlite:///sensorhub.db")
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://") and "+psycopg" not in url:
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url
engine = create_engine(get_database_url())
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
class Base(DeclarativeBase): ...
class SensorModel(Base):
    __tablename__ = "sensors"
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[str] = mapped_column(unique=True, index=True)
    sensor_type: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
class ReadingModel(Base):
    __tablename__ = "readings"
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[str] = mapped_column(index=True)
    value: Mapped[float]
    unit: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    active: Mapped[bool] = mapped_column(default=True)
