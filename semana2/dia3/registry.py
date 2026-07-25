from dataclasses import dataclass


class SensorNotFoundError(Exception):
    """Se lanza cuando se pide un sensor que no está registrado."""


@dataclass(frozen=True)
class SensorReading:
    sensor_id: str
    value: float


class SensorRegistry:
    def __init__(self) -> None:
        self._readings: dict[str, SensorReading] = {}

    def get(self, sensor_id: str) -> SensorReading:
        if sensor_id not in self._readings:
            raise SensorNotFoundError(f"sensor no encontrado: {sensor_id}")
        return self._readings[sensor_id]

    def record(self, reading: SensorReading) -> None:
        self._validate_reading(reading)
        self._readings[reading.sensor_id] = reading

    def _validate_reading(self, reading: SensorReading) -> None:
        if not reading.sensor_id:
            raise ValueError("sensor_id no puede estar vacio")