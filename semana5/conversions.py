def celsius_to_fahrenheit(c: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit, rounded to 2 decimals."""
    return round(c * 9 / 5 + 32, 2)
def fahrenheit_to_celsius(f: float) -> float:
    """Convert a temperature from Fahrenheit to Celsius, rounded to 2 decimals."""
    return round((f - 32) * 5 / 9, 2)
