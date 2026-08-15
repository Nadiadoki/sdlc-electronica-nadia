# Prompting efectivo - Semana 5, Dia 1

## Tarea 1: Conversion de temperatura

### Prompt pobre
"Hazme una funcion que convierta temperatura."

### Resultado del prompt pobre
Ambiguo: no dice de que unidad a cual, no sabe en que archivo va, sin type hints, sin manejo del redondeo.

### Prompt bueno
CONTEXTO: API FastAPI (Python 3.12) para gestion de sensores. SQLAlchemy 2.x tipado, arquitectura en capas.
TAREA: escribe una funcion pura celsius_to_fahrenheit(c: float) -> float en semana5/conversions.py.
RESTRICCIONES: type hints completos, docstring, sin dependencias externas, redondeo a 2 decimales.
ENTREGA: solo la funcion, sin explicacion.

### Resultado del prompt bueno
```python
def celsius_to_fahrenheit(c: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit, rounded to 2 decimals."""
    return round(c * 9 / 5 + 32, 2)
```

## Tarea 2: Validacion de rango fisico

### Prompt pobre
"Valida que el valor del sensor este bien."

### Resultado del prompt pobre
No sabe que significa "bien": que tipo de sensor, que rangos fisicos, en que archivo va. Probablemente inventa rangos genericos incorrectos o pregunta de vuelta.

### Prompt bueno
CONTEXTO: API FastAPI para gestion de sensores. Los sensores son de tipo TEMPERATURE (rango fisico realista -40 a 85 grados C) o HUMIDITY (0 a 100 porciento).
TAREA: escribe una funcion pura is_within_physical_range(value: float, sensor_type: SensorType) -> bool en semana5/validation.py.
RESTRICCIONES: type hints completos, docstring, usa el Enum SensorType ya existente en app/db.py, sin dependencias externas.
ENTREGA: solo la funcion, sin explicacion.

### Resultado del prompt bueno
```python
def is_within_physical_range(value: float, sensor_type: SensorType) -> bool:
    """Return True if value is within the physical range for sensor_type."""
    ranges = {
        SensorType.TEMPERATURE: (-40.0, 85.0),
        SensorType.HUMIDITY: (0.0, 100.0),
    }
    low, high = ranges[sensor_type]
    return low <= value <= high
```
## Tarea 3: Tests para un repositorio

### Prompt pobre
"Escribe tests para mi repositorio de sensores."

### Resultado del prompt pobre
No sabe que framework uso (pytest vs unittest), ni la firma real de los metodos, ni las convenciones del proyecto. Probablemente inventa nombres de metodos o usa mocks innecesarios.

### Prompt bueno
CONTEXTO: API FastAPI con arquitectura en capas. SQLAlchemySensorRepository (en app/repositories/sqlalchemy_sensor_repository.py) tiene metodos add(sensor_id: str, sensor_type: str) y get_by_sensor_id(sensor_id: str) -> SensorModel o None.
TAREA: escribe tests con pytest en semana5/test_sensor_repository.py para get_by_sensor_id() con id existente, get_by_sensor_id() con id inexistente (debe regresar None), y add() con datos validos.
RESTRICCIONES: usa fixtures de pytest, base de datos SQLite en memoria, sin mocks innecesarios.
ENTREGA: solo el codigo de los tests, sin explicacion.

### Resultado del prompt bueno
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.repositories.sqlalchemy_sensor_repository import SQLAlchemySensorRepository


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_get_by_sensor_id_existing_returns_sensor(db_session):
    repo = SQLAlchemySensorRepository(db_session)
    repo.add(sensor_id="TEMP-01", sensor_type="temperature")
    result = repo.get_by_sensor_id("TEMP-01")
    assert result is not None
    assert result.sensor_id == "TEMP-01"


def test_get_by_sensor_id_missing_returns_none(db_session):
    repo = SQLAlchemySensorRepository(db_session)
    assert repo.get_by_sensor_id("GHOST-99") is None


def test_add_with_valid_data_persists_sensor(db_session):
    repo = SQLAlchemySensorRepository(db_session)
    result = repo.add(sensor_id="HUM-01", sensor_type="humidity")
    assert result.sensor_id == "HUM-01"
```
