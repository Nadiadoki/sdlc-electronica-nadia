import pytest

from parsers import ModbusParser, NMEAParser


def test_modbus_parser_frame_valido():
    parser = ModbusParser()
    frame = bytes([0x01, 0x03, 0x02, 0x00, 0x0A, 0xC5, 0xCD])
    resultado = parser.parse(frame)
    assert resultado.protocol == "modbus_rtu"
    assert resultado.payload["address"] == 1


def test_modbus_parser_frame_invalido_lanza_error():
    parser = ModbusParser()
    with pytest.raises(ValueError):
        parser.parse(b"\x01")


def test_nmea_parser_sentencia_valida():
    parser = NMEAParser()
    sentencia = b"$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
    resultado = parser.parse(sentencia)
    assert resultado.protocol == "nmea"
    assert resultado.payload["tipo"] == "GPGGA"


def test_nmea_parser_can_parse_rechaza_modbus():
    parser = NMEAParser()
    assert parser.can_parse(bytes([0x01, 0x03, 0x02])) is False
