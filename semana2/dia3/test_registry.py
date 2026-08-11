import pytest
from registry import SensorNotFoundError, SensorReading, SensorRegistry


def test_get_unknown_sensor_raises():
    registry = SensorRegistry()
    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")
def test_record_and_get_returns_reading():
    registry = SensorRegistry()
    registry.record(SensorReading(sensor_id="TEMP-01", value=24.3))
    resultado = registry.get("TEMP-01")
    assert resultado.value == 24.3
def test_record_rejects_empty_sensor_id():
    registry = SensorRegistry()
    with pytest.raises(ValueError):
        registry.record(SensorReading(sensor_id="", value=24.3))
