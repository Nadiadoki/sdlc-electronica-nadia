import pytest

from app.db import ReadingModel
from app.services.reading_service import ReadingService


class FakeReadingRepository:
    """Repositorio en memoria: cumple el Protocol ReadingRepository sin tocar una base de datos real."""

    def __init__(self) -> None:
        self._readings: list[ReadingModel] = []
        self._next_id = 1

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(id=self._next_id, sensor_id=sensor_id, value=value, unit=unit)
        self._readings.append(reading)
        self._next_id += 1
        return reading

    def list_for_sensor(self, sensor_id: str) -> list[ReadingModel]:
        return [r for r in self._readings if r.sensor_id == sensor_id]


def test_record_guarda_una_lectura_valida():
    service = ReadingService(repo=FakeReadingRepository())
    resultado = service.record(sensor_id="TEMP-01", value=24.5, unit="C")
    assert resultado.sensor_id == "TEMP-01"
    assert resultado.value == 24.5


def test_record_rechaza_temperatura_bajo_el_cero_absoluto():
    service = ReadingService(repo=FakeReadingRepository())
    with pytest.raises(ValueError):
        service.record(sensor_id="TEMP-01", value=-300.0, unit="C")


def test_list_for_sensor_devuelve_solo_las_lecturas_de_ese_sensor():
    repo = FakeReadingRepository()
    service = ReadingService(repo=repo)
    service.record(sensor_id="TEMP-01", value=20.0, unit="C")
    service.record(sensor_id="TEMP-02", value=22.0, unit="C")
    service.record(sensor_id="TEMP-01", value=25.0, unit="C")

    resultado = repo.list_for_sensor("TEMP-01")

    assert len(resultado) == 2
    assert all(r.sensor_id == "TEMP-01" for r in resultado)
