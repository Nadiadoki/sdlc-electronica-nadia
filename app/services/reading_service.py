from datetime import datetime

from app.db import ReadingModel
from app.exceptions import ReadingAlreadyInactiveError, ReadingNotFoundError, SensorNotFoundError
from app.repositories.alert_repository import AlertRepository
from app.repositories.reading_repository import ReadingRepository
from app.repositories.sensor_repository import SensorRepository
from app.strategies import AnomalyDetector, ThresholdExceededStrategy

RANGOS_FISICOS = { 
    "temperature": (-273.15, 1000.0), 
    "humidity": (0.0, 100.0), 
} 
UNIDADES_VALIDAS = { 
    "temperature": "C", 
    "humidity": "%", 
} 
class ReadingService: 
    """Logica de negocio. Depende de abstracciones (DIP): ReadingRepository y SensorRepository.""" 
    def __init__( 
        self, 
        repo: ReadingRepository, 
        sensor_repo: SensorRepository, 
        alert_repo: AlertRepository | None = None, 
        detector: AnomalyDetector | None = None, 
    ) -> None: 
        self._repo = repo 
        self._sensor_repo = sensor_repo 
        self._alert_repo = alert_repo 
        self._detector = detector or AnomalyDetector(strategy=ThresholdExceededStrategy()) 
    def record(self, sensor_id: str, value: float, unit: str) -> ReadingModel: 
        sensor = self._sensor_repo.get_by_sensor_id(sensor_id) 
        if sensor is None: 
            raise SensorNotFoundError(f"sensor no registrado: {sensor_id}") 
        self._validar(sensor.sensor_type, value, unit) 
        reading = self._repo.add(sensor_id, value, unit) 
        if self._alert_repo is not None and sensor.alert_threshold is not None: 
            if self._detector.is_anomaly(value, sensor.alert_threshold): 
                self._alert_repo.add( 
                    sensor_id=sensor_id, 
                    reading_id=reading.id, 
                    value=value, 
                    threshold=sensor.alert_threshold, 
                ) 
        return reading 
    def get_reading(self, reading_id: int) -> ReadingModel: 
        reading = self._repo.get(reading_id) 
        if reading is None: 
            raise ReadingNotFoundError(f"lectura no encontrada: {reading_id}") 
        return reading 
    def list_for_sensor( 
        self, 
        sensor_id: str, 
        limit: int = 50, 
        offset: int = 0, 
        from_: datetime | None = None, 
        to: datetime | None = None, 
    ) -> list[ReadingModel]: 
        if from_ is not None and to is not None and from_ > to: 
            raise ValueError("el rango de fechas es invalido: from es posterior a to") 
        return self._repo.list_for_sensor(sensor_id, limit, offset, from_, to) 
    def update_reading( 
        self, reading_id: int, value: float | None = None, unit: str | None = None 
    ) -> ReadingModel: 
        reading = self._repo.get(reading_id) 
        if reading is None: 
            raise ReadingNotFoundError(f"lectura no encontrada: {reading_id}") 
        if value is not None or unit is not None: 
            sensor = self._sensor_repo.get_by_sensor_id(reading.sensor_id) 
            if sensor is None: 
                raise SensorNotFoundError(f"sensor no registrado: {reading.sensor_id}") 
            valor_final = value if value is not None else reading.value 
            unidad_final = unit if unit is not None else reading.unit 
            self._validar(sensor.sensor_type, valor_final, unidad_final) 
        actualizado = self._repo.update(reading_id, value=value, unit=unit) 
        if actualizado is None: 
            raise ReadingNotFoundError(f"lectura no encontrada: {reading_id}") 
        return actualizado 
    def deactivate_reading(self, reading_id: int) -> None: 
        if self._repo.get(reading_id) is None: 
            raise ReadingNotFoundError(f"lectura no encontrada: {reading_id}") 
        if not self._repo.deactivate(reading_id): 
            raise ReadingAlreadyInactiveError(f"lectura ya estaba inactiva: {reading_id}") 
    def _validar(self, sensor_type: str, value: float, unit: str) -> None: 
        unidad_esperada = UNIDADES_VALIDAS[sensor_type] 
        if unit != unidad_esperada: 
            raise ValueError( 
                f"unidad '{unit}' no valida para sensor tipo {sensor_type}; " 
                f"se esperaba '{unidad_esperada}'" 
            ) 
        minimo, maximo = RANGOS_FISICOS[sensor_type] 
        if not (minimo <= value <= maximo): 
            raise ValueError( 
                f"valor {value} fuera de rango fisico para {sensor_type} ({minimo}..{maximo})" 
            ) 
