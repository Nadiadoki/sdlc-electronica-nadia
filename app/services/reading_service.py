from datetime import datetime

from app.db import ReadingModel
from app.repositories.reading_repository import ReadingRepository

CERO_ABSOLUTO = -273.15


class ReadingNotFoundError(Exception):
    """La lectura solicitada no existe."""


class ReadingAlreadyInactiveError(Exception):
    """La lectura ya estaba desactivada; no se puede desactivar de nuevo."""


class ReadingService:
    """Logica de negocio. Depende de la abstraccion del repositorio (DIP)."""

    def __init__(self, repo: ReadingRepository) -> None:
        self._repo = repo

    def record(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        self._validar_valor(value)
        return self._repo.add(sensor_id, value, unit)

    def get_reading(self, reading_id: int) -> ReadingModel:
        reading = self._repo.get(reading_id)
        if reading is None:
            raise ReadingNotFoundError(f"lectura no encontrada: {reading_id}")
        return reading

    def list_for_sensor(
        self,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        from_: datetime | None = None,
        to: datetime | None = None,
    ) -> list[ReadingModel]:
        if from_ is not None and to is not None and from_ > to:
            raise ValueError("el rango de fechas es invalido: from es posterior a to")
        return self._repo.list_for_sensor(sensor_id, limit, offset, from_, to)

    def update_reading(
        self, reading_id: int, value: float | None = None, unit: str | None = None
    ) -> ReadingModel:
        if value is not None:
            self._validar_valor(value)
        reading = self._repo.update(reading_id, value=value, unit=unit)
        if reading is None:
            raise ReadingNotFoundError(f"lectura no encontrada: {reading_id}")
        return reading

    def deactivate_reading(self, reading_id: int) -> None:
        if self._repo.get(reading_id) is None:
            raise ReadingNotFoundError(f"lectura no encontrada: {reading_id}")
        if not self._repo.deactivate(reading_id):
            raise ReadingAlreadyInactiveError(f"lectura ya estaba inactiva: {reading_id}")

    def _validar_valor(self, value: float) -> None:
        if value < CERO_ABSOLUTO:
            raise ValueError("Temperatura por debajo del cero absoluto")
