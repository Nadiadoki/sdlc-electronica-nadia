from sensors import SensorReading, SensorType
from anomaly import AnomalyDetector


def test_temperatura_dentro_del_rango_no_es_anomalia():
    detector = AnomalyDetector(threshold=35.0)
    lectura = SensorReading(sensor_id="TEMP-01", sensor_type=SensorType.TEMPERATURE, value=30.0)
    assert detector.is_anomaly(lectura) is False


def test_temperatura_supera_el_umbral_es_anomalia():
    detector = AnomalyDetector(threshold=35.0)
    lectura = SensorReading(sensor_id="TEMP-01", sensor_type=SensorType.TEMPERATURE, value=38.2)
    assert detector.is_anomaly(lectura) is True


def test_temperatura_exactamente_en_el_umbral_no_es_anomalia():
    detector = AnomalyDetector(threshold=35.0)
    lectura = SensorReading(sensor_id="TEMP-01", sensor_type=SensorType.TEMPERATURE, value=35.0)
    assert detector.is_anomaly(lectura) is False


def test_humedad_supera_el_umbral_es_anomalia():
    detector = AnomalyDetector(threshold=80.0)
    lectura = SensorReading(sensor_id="HUM-02", sensor_type=SensorType.HUMIDITY, value=85.0)
    assert detector.is_anomaly(lectura) is True


def test_humedad_dentro_del_rango_no_es_anomalia():
    detector = AnomalyDetector(threshold=80.0)
    lectura = SensorReading(sensor_id="HUM-02", sensor_type=SensorType.HUMIDITY, value=60.0)
    assert detector.is_anomaly(lectura) is False