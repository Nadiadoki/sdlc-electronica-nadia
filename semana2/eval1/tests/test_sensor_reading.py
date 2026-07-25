import pytest
from sensors import SensorReading, SensorType


def test_registrar_lectura_temperatura_valida():
    lectura = SensorReading(sensor_id="TEMP-03", sensor_type=SensorType.TEMPERATURE, value=24.5)
    assert lectura.sensor_id == "TEMP-03"
    assert lectura.value == 24.5
    assert lectura.sensor_type == SensorType.TEMPERATURE


def test_rechazar_temperatura_fuera_de_rango():
    with pytest.raises(ValueError):
        SensorReading(sensor_id="TEMP-03", sensor_type=SensorType.TEMPERATURE, value=-500.0)