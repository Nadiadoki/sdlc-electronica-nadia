"""
Día 4 · SOLID completo: I y D — dominio de sensores.
"""
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SensorReading:
    sensor_id: str
    value: float


# ---------------------------------------------------------------------
# I - Interface Segregation: interfaces chicas, no una gorda.
# ---------------------------------------------------------------------

# MAL: una interfaz gorda obliga a implementar métodos que no necesitas.
class SensorDeviceMal(Protocol):
    def read(self) -> SensorReading: ...
    def write(self, config: dict) -> None: ...
    def calibrate(self, offset: float) -> None: ...
    def reset(self) -> None: ...
# Un sensor de solo lectura tendría que "implementar" write/calibrate/reset
# aunque no tengan sentido para él -> viola ISP.


# BIEN: interfaces chicas y específicas.
class Readable(Protocol):
    def read(self) -> SensorReading: ...


class Writable(Protocol):
    def write(self, config: dict) -> None: ...


class Calibratable(Protocol):
    def calibrate(self, offset: float) -> None: ...


class SimpleSensor:
    """Solo lee: solo necesita cumplir Readable."""
    def read(self) -> SensorReading:
        return SensorReading(sensor_id="s1", value=23.5)


class AdvancedSensor:
    """Lee y se calibra: cumple Readable + Calibratable, nada más."""
    def __init__(self) -> None:
        self._offset = 0.0

    def read(self) -> SensorReading:
        return SensorReading(sensor_id="s2", value=23.5 + self._offset)

    def calibrate(self, offset: float) -> None:
        self._offset = offset


# ---------------------------------------------------------------------
# D - Dependency Inversion: depender de abstracciones, no de concreciones.
# ---------------------------------------------------------------------

class DataRepository(Protocol):
    def save(self, reading: SensorReading) -> None: ...
    def get_latest(self, sensor_id: str) -> SensorReading | None: ...


# MAL: acoplado directamente a una implementación concreta.
class PostgreSQLRepositoryMal:
    def save(self, reading: SensorReading) -> None:
        pass  # conexión real a base de datos...

    def get_latest(self, sensor_id: str) -> SensorReading | None:
        return None


class DataProcessorMal:
    def __init__(self) -> None:
        self._repo = PostgreSQLRepositoryMal()  # sin inyección: no es testeable


# BIEN: DataProcessor depende de la abstracción, no de una implementación.
class InMemoryRepository:
    """Sin base de datos real: ideal para tests."""
    def __init__(self) -> None:
        self._data: dict[str, SensorReading] = {}

    def save(self, reading: SensorReading) -> None:
        self._data[reading.sensor_id] = reading

    def get_latest(self, sensor_id: str) -> SensorReading | None:
        return self._data.get(sensor_id)


class DataProcessor:
    """Depende de la abstracción (DataRepository), no de una implementación concreta."""
    def __init__(self, repository: DataRepository) -> None:
        self._repo = repository  # inyección de dependencias

    def process(self, reading: SensorReading) -> None:
        self._repo.save(reading)

    def latest_for(self, sensor_id: str) -> SensorReading | None:
        return self._repo.get_latest(sensor_id)


# En producción: DataProcessor(PostgreSQLRepository())
# En tests:       DataProcessor(InMemoryRepository())  <- sin base de datos
