from sensors import SensorReading, SensorType


def test_registrar_lectura_temperatura_valida():
    lectura = SensorReading(sensor_id="TEMP-03", sensor_type=SensorType.TEMPERATURE, value=24.5)
    assert lectura.sensor_id == "TEMP-03"
    assert lectura.value == 24.5
    assert lectura.sensor_type == SensorType.TEMPERATURE