from alerts import ConsoleAlert


def test_console_alert_imprime_el_mensaje(capsys):
    alert = ConsoleAlert()
    alert.send("Anomalia en TEMP-01: 40.0")
    salida = capsys.readouterr().out
    assert "Anomalia en TEMP-01: 40.0" in salida


def test_file_alert_escribe_en_archivo(tmp_path):
    from alerts import FileAlert

    path = tmp_path / "alertas.log"
    alert = FileAlert(path=str(path))
    alert.send("Anomalia en HUM-02: 88.0")
    assert "Anomalia en HUM-02: 88.0" in path.read_text()

def test_alert_manager_dispara_alerta_en_anomalia():
    from alert_manager import AlertManager
    from anomaly import AnomalyDetector
    from sensors import SensorReading, SensorType

    mensajes = []

    class AlertaDePrueba:
        def send(self, message: str) -> None:
            mensajes.append(message)

    manager = AlertManager(detector=AnomalyDetector(threshold=35.0), alert=AlertaDePrueba())
    lectura = SensorReading(sensor_id="TEMP-01", sensor_type=SensorType.TEMPERATURE, value=40.0)
    manager.process(lectura)

    assert len(mensajes) == 1
    assert "TEMP-01" in mensajes[0]


def test_alert_manager_no_dispara_alerta_sin_anomalia():
    from alert_manager import AlertManager
    from anomaly import AnomalyDetector
    from sensors import SensorReading, SensorType

    mensajes = []

    class AlertaDePrueba:
        def send(self, message: str) -> None:
            mensajes.append(message)

    manager = AlertManager(detector=AnomalyDetector(threshold=35.0), alert=AlertaDePrueba())
    lectura = SensorReading(sensor_id="TEMP-01", sensor_type=SensorType.TEMPERATURE, value=20.0)
    manager.process(lectura)

    assert len(mensajes) == 0