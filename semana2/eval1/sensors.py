from dataclasses import dataclass
from enum import Enum, auto


class SensorType(Enum):
    TEMPERATURE = auto()
    HUMIDITY = auto()


@dataclass(frozen=True)
class SensorReading:
    sensor_id: str
    sensor_type: SensorType
    value: float