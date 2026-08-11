from alerts import AlertStrategy
from anomaly import AnomalyDetector
from sensors import SensorReading


class AlertManager:
    """Orquesta la deteccion de anomalias con el envio de alertas.

    Depende de una abstraccion (cualquier objeto con .send(message)),
    no de una implementacion concreta -- puede recibir ConsoleAlert,
    FileAlert, o cualquier otra estrategia que respete la interfaz.
    """

    def __init__(self, detector: AnomalyDetector, alert: AlertStrategy) -> None:
        self._detector = detector
        self._alert = alert

    def process(self, reading: SensorReading) -> None:
        if self._detector.is_anomaly(reading):
            self._alert.send(f"Anomalia en {reading.sensor_id}: {reading.value}")