"""
Día 3 · SOLID en la práctica: S, O y L — dominio de sensores.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class SensorReading:
    sensor_id: str
    value: float


# ---------------------------------------------------------------------
# S - Single Responsibility: una clase, una responsabilidad.
# ---------------------------------------------------------------------

# MAL: una sola clase lee Y persiste -> dos razones distintas para cambiar.
class SensorHandlerMal:
    def read(self) -> SensorReading:
        return SensorReading(sensor_id="s1", value=23.5)

    def save(self, reading: SensorReading, path: str = "log.txt") -> None:
        with open(path, "a") as f:
            f.write(f"{reading.sensor_id}:{reading.value}\n")


# BIEN: SensorReader lee; DataLogger persiste.
class SensorReader:
    def read(self) -> SensorReading:
        return SensorReading(sensor_id="s1", value=23.5)


class DataLogger:
    def save(self, reading: SensorReading, path: str = "log.txt") -> None:
        with open(path, "a") as f:
            f.write(f"{reading.sensor_id}:{reading.value}\n")


# ---------------------------------------------------------------------
# O - Open/Closed: abierto a extensión, cerrado a modificación.
# ---------------------------------------------------------------------

# MAL: agregar un nuevo tipo de alerta obliga a MODIFICAR esta función.
def enviar_alerta_mal(tipo: str, mensaje: str) -> str:
    if tipo == "console":
        return f"[CONSOLE] {mensaje}"
    elif tipo == "file":
        return f"[FILE] {mensaje}"
    raise ValueError(f"tipo desconocido: {tipo}")  # agregar "email" rompe esto


# BIEN: AlertStrategy (ABC); agregar EmailAlert mañana no toca el código existente.
class AlertStrategy(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...


class ConsoleAlert(AlertStrategy):
    def send(self, message: str) -> None:
        print(f"[CONSOLE] {message}")


class FileAlert(AlertStrategy):
    def __init__(self, path: str = "alerts.log") -> None:
        self._path = path

    def send(self, message: str) -> None:
        with open(self._path, "a") as f:
            f.write(message + "\n")


class AnomalyDetector:
    def __init__(self, alert: AlertStrategy, threshold: float) -> None:
        self._alert = alert
        self._threshold = threshold

    def check(self, reading: SensorReading) -> None:
        if reading.value > self._threshold:
            self._alert.send(f"Anomalia en {reading.sensor_id}")


# ---------------------------------------------------------------------
# L - Liskov Substitution: las subclases deben ser intercambiables.
# ---------------------------------------------------------------------

class BaseSensor(ABC):
    @abstractmethod
    def read(self) -> SensorReading: ...


# MAL: exige un parámetro extra que BaseSensor.read() no promete ->
# ya no es sustituible donde se espera un BaseSensor.
class HumiditySensorMal(BaseSensor):
    def read(self, calibration_offset: float) -> SensorReading:  # type: ignore[override]
        return SensorReading(sensor_id="h1", value=55.0 + calibration_offset)


# BIEN: TemperatureSensor y HumiditySensor son intercambiables.
class TemperatureSensor(BaseSensor):
    def read(self) -> SensorReading:
        return SensorReading(sensor_id="t1", value=23.5)


class HumiditySensor(BaseSensor):
    def read(self) -> SensorReading:
        return SensorReading(sensor_id="h1", value=55.0)


def process_sensor(sensor: BaseSensor) -> SensorReading:
    """Funciona con cualquier BaseSensor, sin importar cuál sea."""
    return sensor.read()
