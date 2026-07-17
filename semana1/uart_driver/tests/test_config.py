import pytest

from config import UartConfig


def test_baudrate_valido_se_acepta():
    cfg = UartConfig(baudrate=9600)
    assert cfg.baudrate == 9600


def test_baudrate_invalido_lanza_error():
    with pytest.raises(ValueError):
        UartConfig(baudrate=1234)


def test_config_es_inmutable():
    cfg = UartConfig(baudrate=9600)
    with pytest.raises(AttributeError):
        cfg.baudrate = 19200  # type: ignore[misc]
