"""
config.py — SRP + inmutabilidad.
Única responsabilidad: representar y validar la configuración del puerto UART.
"""
from dataclasses import dataclass
from typing import Literal

BAUDRATES_VALIDOS = {9600, 19200, 38400, 57600, 115200}
STOP_BITS_VALIDOS = {1.0, 1.5, 2.0}


@dataclass(frozen=True)
class UartConfig:
    baudrate: int
    parity: Literal["N", "E", "O"] = "N"
    stop_bits: float = 1.0
    timeout: float = 1.0

    def __post_init__(self) -> None:
        if self.baudrate not in BAUDRATES_VALIDOS:
            raise ValueError(f"baudrate invalido: {self.baudrate}")
        if self.parity not in ("N", "E", "O"):
            raise ValueError(f"parity invalido: {self.parity}")
        if self.stop_bits not in STOP_BITS_VALIDOS:
            raise ValueError(f"stop_bits invalido: {self.stop_bits}")
        if self.timeout <= 0:
            raise ValueError(f"timeout debe ser positivo: {self.timeout}")
