from app.db import ReadingModel
from app.repositories.reading_repository import ReadingRepository

CERO_ABSOLUTO = -273.15


class ReadingService:
    """Logica de negocio. Depende de la abstraccion del repositorio (DIP)."""

    def __init__(self, repo: ReadingRepository) -> None:
        self._repo = repo

    def record(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        if value < CERO_ABSOLUTO:
            raise ValueError("Temperatura por debajo del cero absoluto")
        return self._repo.add(sensor_id, value, unit)
