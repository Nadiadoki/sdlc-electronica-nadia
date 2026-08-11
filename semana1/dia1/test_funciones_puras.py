import pytest
from funciones_puras import (
    celsius_a_fahrenheit,
    diferencia_valor,
    es_valida,
    serializar_reading,
    supera_umbral,
)
from lectura import Reading, SensorType


def test_celsius_a_fahrenheit():
    assert celsius_a_fahrenheit(0) == 32
    assert celsius_a_fahrenheit(100) == 212


def test_supera_umbral():
    r = Reading("s1", 30.0, SensorType.TEMPERATURE)
    assert supera_umbral(r, 25.0) is True
    assert supera_umbral(r, 35.0) is False


def test_es_valida():
    r = Reading("s1", 23.5, SensorType.TEMPERATURE)
    assert es_valida(r, -40, 125) is True
    assert es_valida(r, 24, 30) is False


def test_serializar_reading():
    r = Reading("s1", 23.5, SensorType.TEMPERATURE)
    assert serializar_reading(r) == "[TEMPERATURE] s1 = 23.50"


def test_diferencia_valor():
    a = Reading("s1", 30.0, SensorType.TEMPERATURE)
    b = Reading("s1", 20.0, SensorType.TEMPERATURE)
    assert diferencia_valor(a, b) == 10.0


def test_diferencia_valor_tipos_distintos():
    a = Reading("s1", 30.0, SensorType.TEMPERATURE)
    b = Reading("s2", 50.0, SensorType.HUMIDITY)
    with pytest.raises(ValueError):
        diferencia_valor(a, b)
