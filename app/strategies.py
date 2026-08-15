from typing import Protocol


class AlertStrategy(Protocol): 
    def evaluate(self, value: float, threshold: float) -> bool: ... 
 
 
class ThresholdExceededStrategy: 
    """Dispara si el valor supera estrictamente el umbral.""" 
 
    def evaluate(self, value: float, threshold: float) -> bool: 
        return value > threshold 
 
 
class AnomalyDetector: 
    """Decide si una lectura es anomala, usando una estrategia intercambiable (OCP).""" 
 
    def __init__(self, strategy: AlertStrategy) -> None: 
        self._strategy = strategy 
 
    def is_anomaly(self, value: float, threshold: float) -> bool: 
        return self._strategy.evaluate(value, threshold) 
