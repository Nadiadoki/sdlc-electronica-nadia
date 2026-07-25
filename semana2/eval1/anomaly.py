from sensors import SensorReading


class AnomalyDetector:
    """Detecta anomalias comparando una lectura contra un umbral inyectado."""

    def __init__(self, threshold: float) -> None:
        self._threshold = threshold

    @property
    def threshold(self) -> float:
        return self._threshold

    @threshold.setter
    def threshold(self, value: float) -> None:
        self._threshold = value

    def is_anomaly(self, reading: SensorReading) -> bool:
        return reading.value > self._threshold