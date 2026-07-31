import pytest

from app.db import SensorModel
from app.exceptions import SensorAlreadyExistsError, SensorAlreadyInactiveError, SensorNotFoundError
from app.services.sensor_service import SensorService


class FakeSensorRepository:
    def __init__(self) -> None:
        self._sensores: dict[str, SensorModel] = {}

    def add(self, sensor_id: str, sensor_type: str) -> SensorModel:
        sensor = SensorModel(sensor_id=sensor_id, sensor_type=sensor_type, active=True)
        self._sensores[sensor_id] = sensor
        return sensor

    def get_by_sensor_id(self, sensor_id: str):
        return self._sensores.get(sensor_id)

    def list(self, limit=50, offset=0):
        return list(self._sensores.values())[offset : offset + limit]

    def update(self, sensor_id: str, sensor_type=None):
        sensor = self._sensores.get(sensor_id)
        if sensor is None:
            return None
        if sensor_type is not None:
            sensor.sensor_type = sensor_type
        return sensor

    def deactivate(self, sensor_id: str) -> bool:
        sensor = self._sensores.get(sensor_id)
        if sensor is None or not sensor.active:
            return False
        sensor.active = False
        return True


def test_create_registra_un_sensor_nuevo():
    service = SensorService(repo=FakeSensorRepository())
    sensor = service.create("TEMP-01", "temperature")
    assert sensor.sensor_id == "TEMP-01"
    assert sensor.sensor_type == "temperature"


def test_create_rechaza_sensor_duplicado():
    service = SensorService(repo=FakeSensorRepository())
    service.create("TEMP-01", "temperature")
    with pytest.raises(SensorAlreadyExistsError):
        service.create("TEMP-01", "temperature")


def test_create_rechaza_tipo_invalido():
    service = SensorService(repo=FakeSensorRepository())
    with pytest.raises(ValueError):
        service.create("TEMP-01", "pressure")


def test_get_sensor_inexistente_lanza_error():
    service = SensorService(repo=FakeSensorRepository())
    with pytest.raises(SensorNotFoundError):
        service.get("GHOST-99")


def test_deactivate_dos_veces_lanza_error():
    service = SensorService(repo=FakeSensorRepository())
    service.create("TEMP-01", "temperature")
    service.deactivate("TEMP-01")
    with pytest.raises(SensorAlreadyInactiveError):
        service.deactivate("TEMP-01")
