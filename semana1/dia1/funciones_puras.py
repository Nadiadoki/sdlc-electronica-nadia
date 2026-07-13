"""
Ejercicio Día 1: 5 funciones puras sobre Reading.
Todas reciben datos, no tienen efectos secundarios y devuelven un nuevo valor.
Verificar con: mypy funciones_puras.py  /  ruff check funciones_puras.py
"""
from lectura import Reading


def celsius_a_fahrenheit(valor_c: float) -> float:
    """Conversión de unidades: C -> F."""
    return valor_c * 9 / 5 + 32


def supera_umbral(r: Reading, umbral: float) -> bool:
    """Detección de umbral simple."""
    return r.value > umbral


def es_valida(r: Reading, minimo: float, maximo: float) -> bool:
    """Validación de rango. El rango se pasa como parámetro:
    no debe estar hardcodeado porque depende del SensorType real."""
    return minimo <= r.value <= maximo


def serializar_reading(r: Reading) -> str:
    """Serialización a texto legible (no confundir con to_frame,
    que serializa a bytes para transporte)."""
    return f"[{r.sensor_type.name}] {r.sensor_id} = {r.value:.2f}"


def diferencia_valor(a: Reading, b: Reading) -> float:
    """Comparación entre dos lecturas del mismo tipo de sensor."""
    if a.sensor_type != b.sensor_type:
        raise ValueError("no se pueden comparar sensores de distinto tipo")
    return a.value - b.value
