import pytest
from solid_srp_ocp_lsp import (
    AlertStrategy,
    AnomalyDetector,
    ConsoleAlert,
    DataLogger,
    HumiditySensor,
    HumiditySensorMal,
    SensorReader,
    SensorReading,
    TemperatureSensor,
    process_sensor,
)

# --- S: Single Responsibility ---

def test_sensor_reader_solo_lee():
    reader = SensorReader()
    reading = reader.read()
    assert isinstance(reading, SensorReading)
    assert reading.sensor_id == "s1"


def test_data_logger_solo_persiste(tmp_path):
    path = tmp_path / "log.txt"
    logger = DataLogger()
    logger.save(SensorReading("s1", 23.5), path=str(path))
    assert "s1:23.5" in path.read_text()


# --- O: Open/Closed ---

def test_anomaly_detector_dispara_alerta(capsys):
    detector = AnomalyDetector(alert=ConsoleAlert(), threshold=20.0)
    detector.check(SensorReading("s1", 30.0))
    assert "Anomalia en s1" in capsys.readouterr().out


def test_nueva_alerta_sin_modificar_anomaly_detector(capsys):
    """Extensión real: una alerta nueva se agrega sin tocar AnomalyDetector."""
    class EmailAlert(AlertStrategy):
        def send(self, message: str) -> None:
            print(f"[EMAIL] {message}")

    detector = AnomalyDetector(alert=EmailAlert(), threshold=20.0)
    detector.check(SensorReading("s1", 30.0))
    assert "[EMAIL] Anomalia en s1" in capsys.readouterr().out


# --- L: Liskov Substitution ---

def test_process_sensor_es_intercambiable():
    assert process_sensor(TemperatureSensor()).sensor_id == "t1"
    assert process_sensor(HumiditySensor()).sensor_id == "h1"


def test_humidity_sensor_mal_rompe_la_sustitucion():
    """HumiditySensorMal exige un argumento extra: no es sustituible por BaseSensor."""
    with pytest.raises(TypeError):
        process_sensor(HumiditySensorMal())
