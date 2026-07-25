from sensors import SensorReading


class AnomalyDetector:
    """Detecta anomalias comparando una lectura contra un umbral inyectado."""

    def __init__(self, threshold: float) -> None:
        self._threshold = threshold

    def is_anomaly(self, reading: SensorReading) -> bool:
        return reading.value > self._threshold