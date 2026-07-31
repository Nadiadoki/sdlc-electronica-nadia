from app.db import SensorModel
from app.exceptions import SensorAlreadyExistsError, SensorAlreadyInactiveError, SensorNotFoundError
from app.repositories.sensor_repository import SensorRepository

TIPOS_VALIDOS = {"temperature", "humidity"}


class SensorService:
    def __init__(self, repo: SensorRepository) -> None:
        self._repo = repo

    def create(self, sensor_id: str, sensor_type: str) -> SensorModel:
        if sensor_type not in TIPOS_VALIDOS:
            raise ValueError(f"tipo de sensor invalido: {sensor_type}")
        if self._repo.get_by_sensor_id(sensor_id) is not None:
            raise SensorAlreadyExistsError(f"ya existe un sensor con id: {sensor_id}")
        return self._repo.add(sensor_id, sensor_type)

    def get(self, sensor_id: str) -> SensorModel:
        sensor = self._repo.get_by_sensor_id(sensor_id)
        if sensor is None:
            raise SensorNotFoundError(f"sensor no encontrado: {sensor_id}")
        return sensor

    def list(self, limit: int = 50, offset: int = 0) -> list[SensorModel]:
        return self._repo.list(limit, offset)

    def update(self, sensor_id: str, sensor_type: str | None = None) -> SensorModel:
        if sensor_type is not None and sensor_type not in TIPOS_VALIDOS:
            raise ValueError(f"tipo de sensor invalido: {sensor_type}")
        sensor = self._repo.update(sensor_id, sensor_type=sensor_type)
        if sensor is None:
            raise SensorNotFoundError(f"sensor no encontrado: {sensor_id}")
        return sensor

    def deactivate(self, sensor_id: str) -> None:
        if self._repo.get_by_sensor_id(sensor_id) is None:
            raise SensorNotFoundError(f"sensor no encontrado: {sensor_id}")
        if not self._repo.deactivate(sensor_id):
            raise SensorAlreadyInactiveError(f"sensor ya estaba inactivo: {sensor_id}")
