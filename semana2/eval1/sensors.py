from dataclasses import dataclass
from enum import Enum, auto

RANGO_TEMPERATURA = (-40.0, 125.0)
RANGO_HUMEDAD = (0.0, 100.0)


class SensorType(Enum):
    TEMPERATURE = auto()
    HUMIDITY = auto()


@dataclass(frozen=True)
class SensorReading:
    sensor_id: str
    sensor_type: SensorType
    value: float

    def __post_init__(self) -> None:
        minimo, maximo = (
            RANGO_TEMPERATURA if self.sensor_type == SensorType.TEMPERATURE else RANGO_HUMEDAD
        )
        if not (minimo <= self.value <= maximo):
            raise ValueError(
                f"valor fuera de rango para {self.sensor_type.name}: {self.value}"
            )