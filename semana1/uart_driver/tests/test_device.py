import pytest

from config import UartConfig
from device import UartDevice
from parsers import ModbusParser


class FakePort:
    """Puerto falso: no toca hardware real, ideal para tests."""
    def __init__(self, data: bytes) -> None:
        self._data = data
        self._abierto = False

    def open(self) -> None:
        self._abierto = True

    def close(self) -> None:
        self._abierto = False

    def is_open(self) -> bool:
        return self._abierto

    def read(self) -> bytes:
        return self._data


def test_read_and_parse_sin_conectar_lanza_error():
    frame = bytes([0x01, 0x03, 0x02, 0x00, 0x0A, 0xC5, 0xCD])
    device = UartDevice(UartConfig(baudrate=9600), ModbusParser(), FakePort(frame))
    with pytest.raises(RuntimeError):
        device.read_and_parse()


def test_connect_y_read_and_parse():
    frame = bytes([0x01, 0x03, 0x02, 0x00, 0x0A, 0xC5, 0xCD])
    device = UartDevice(UartConfig(baudrate=9600), ModbusParser(), FakePort(frame))
    device.connect()
    resultado = device.read_and_parse()
    assert resultado.protocol == "modbus_rtu"


def test_disconnect_cierra_el_puerto():
    frame = bytes([0x01, 0x03, 0x02, 0x00, 0x0A, 0xC5, 0xCD])
    port = FakePort(frame)
    device = UartDevice(UartConfig(baudrate=9600), ModbusParser(), port)
    device.connect()
    device.disconnect()
    assert port.is_open() is False
