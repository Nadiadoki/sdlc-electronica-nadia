import pytest

from app.db import ReadingModel, SensorModel
from app.services.reading_service import ReadingService


class FakeReadingRepository:
    """Repositorio en memoria: cumple el Protocol ReadingRepository, sin BD real."""

    def __init__(self) -> None:
        self._readings: list[ReadingModel] = []
        self._next_id = 1

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(id=self._next_id, sensor_id=sensor_id, value=value, unit=unit)
        self._readings.append(reading)
        self._next_id += 1
        return reading

    def get(self, reading_id: int) -> ReadingModel | None:
        return next((r for r in self._readings if r.id == reading_id), None)

    def list_for_sensor(self, sensor_id, limit=50, offset=0, from_=None, to=None):
        return [r for r in self._readings if r.sensor_id == sensor_id]

    def update(self, reading_id, value=None, unit=None):
        reading = self.get(reading_id)
        if reading is None:
            return None
        if value is not None:
            reading.value = value
        if unit is not None:
            reading.unit = unit
        return reading

    def deactivate(self, reading_id):
        reading = self.get(reading_id)
        if reading is None:
            return False
        return True


class FakeSensorRepository:
    """Repositorio en memoria con dos sensores de temperatura ya registrados."""

    def __init__(self) -> None:
        self._sensores = {
            "TEMP-01": SensorModel(sensor_id="TEMP-01", sensor_type="temperature"),
            "TEMP-02": SensorModel(sensor_id="TEMP-02", sensor_type="temperature"),
        }

    def get_by_sensor_id(self, sensor_id):
        return self._sensores.get(sensor_id)


def test_record_guarda_una_lectura_valida():
    service = ReadingService(repo=FakeReadingRepository(), sensor_repo=FakeSensorRepository())
    resultado = service.record(sensor_id="TEMP-01", value=24.5, unit="C")
    assert resultado.sensor_id == "TEMP-01"
    assert resultado.value == 24.5


def test_record_rechaza_temperatura_bajo_el_cero_absoluto():
    service = ReadingService(repo=FakeReadingRepository(), sensor_repo=FakeSensorRepository())
    with pytest.raises(ValueError):
        service.record(sensor_id="TEMP-01", value=-300.0, unit="C")


def test_record_rechaza_unidad_desconocida_para_el_tipo_de_sensor():
    service = ReadingService(repo=FakeReadingRepository(), sensor_repo=FakeSensorRepository())
    with pytest.raises(ValueError):
        service.record(sensor_id="TEMP-01", value=24.5, unit="%")


def test_list_for_sensor_devuelve_solo_las_lecturas_de_ese_sensor():
    repo = FakeReadingRepository()
    service = ReadingService(repo=repo, sensor_repo=FakeSensorRepository())
    service.record(sensor_id="TEMP-01", value=20.0, unit="C")
    service.record(sensor_id="TEMP-02", value=22.0, unit="C")
    service.record(sensor_id="TEMP-01", value=25.0, unit="C")

    resultado = repo.list_for_sensor("TEMP-01")

    assert len(resultado) == 2
    assert all(r.sensor_id == "TEMP-01" for r in resultado)
