import random

from sensors import SensorReading, SensorType


class SensorSimulator:
    """Genera lecturas simuladas para un grupo de sensores usando distribucion gaussiana."""

    def __init__(
        self,
        sensor_ids: list[str],
        sensor_type: SensorType,
        mean: float,
        stddev: float,
        seed: int | None = None,
    ) -> None:
        self._sensor_ids = sensor_ids
        self._sensor_type = sensor_type
        self._mean = mean
        self._stddev = stddev
        self._random = random.Random(seed)

    def generate_cycle(self) -> list[SensorReading]:
        lecturas = []
        for sensor_id in self._sensor_ids:
            valor = self._random.gauss(self._mean, self._stddev)
            lecturas.append(
                SensorReading(sensor_id=sensor_id, sensor_type=self._sensor_type, value=valor)
            )
        return lecturas