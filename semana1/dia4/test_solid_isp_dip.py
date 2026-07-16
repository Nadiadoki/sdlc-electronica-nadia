from solid_isp_dip import (
    SensorReading,
    SimpleSensor,
    AdvancedSensor,
    DataProcessor,
    InMemoryRepository,
)


# --- I: Interface Segregation ---

def test_simple_sensor_solo_lee():
    sensor = SimpleSensor()
    reading = sensor.read()
    assert isinstance(reading, SensorReading)
    assert not hasattr(sensor, "calibrate")


def test_advanced_sensor_lee_y_calibra():
    sensor = AdvancedSensor()
    sensor.calibrate(1.5)
    reading = sensor.read()
    assert reading.value == 23.5 + 1.5


# --- D: Dependency Inversion ---

def test_data_processor_usa_repository_en_memoria():
    repo = InMemoryRepository()
    processor = DataProcessor(repository=repo)
    processor.process(SensorReading("s1", 30.0))
    assert processor.latest_for("s1") == SensorReading("s1", 30.0)


def test_data_processor_no_conoce_implementacion_concreta():
    """DataProcessor funciona igual sin importar qué repositorio reciba."""
    class OtroRepoFake:
        def __init__(self) -> None:
            self._saved: SensorReading | None = None

        def save(self, reading: SensorReading) -> None:
            self._saved = reading

        def get_latest(self, sensor_id: str) -> SensorReading | None:
            return self._saved

    processor = DataProcessor(repository=OtroRepoFake())
    processor.process(SensorReading("s2", 55.0))
    resultado = processor.latest_for("s2")
    assert resultado is not None
    assert resultado.value == 55.0
