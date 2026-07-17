"""
device.py — DIP.
UartDevice depende de las abstracciones MessageParser y SerialPort, no de
implementaciones concretas. Por eso se puede testear con un puerto falso,
sin hardware real y sin instanciar dos veces nada global.
"""
from typing import Protocol

from config import UartConfig
from parsers import MessageParser, ParsedMessage


class SerialPort(Protocol):
    """Abstraccion del puerto fisico: permite inyectar un fake en tests."""
    def open(self) -> None: ...
    def close(self) -> None: ...
    def is_open(self) -> bool: ...
    def read(self) -> bytes: ...


class UartDevice:
    """Recibe config y parser por inyeccion de dependencias."""

    def __init__(self, config: UartConfig, parser: MessageParser, port: SerialPort) -> None:
        self._config = config
        self._parser = parser
        self._port = port

    def connect(self) -> None:
        self._port.open()

    def disconnect(self) -> None:
        self._port.close()

    def read_and_parse(self) -> ParsedMessage:
        if not self._port.is_open():
            raise RuntimeError("dispositivo no conectado")
        raw = self._port.read()
        return self._parser.parse(raw)
