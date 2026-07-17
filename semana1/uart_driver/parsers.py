"""
parsers.py — OCP, LSP, ISP.
Agregar un protocolo nuevo = una clase nueva de MessageParser, sin tocar las existentes (OCP).
ModbusParser y NMEAParser son intercambiables donde se espera un MessageParser (LSP).
La interfaz es chica: solo parse() y can_parse(), nada de más (ISP).
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ParsedMessage:
    protocol: str
    payload: dict[str, Any]


class MessageParser(ABC):
    @abstractmethod
    def can_parse(self, raw: bytes) -> bool: ...

    @abstractmethod
    def parse(self, raw: bytes) -> ParsedMessage: ...


class ModbusParser(MessageParser):
    """Parsea frames Modbus RTU: [addr][func][data...][crc_lo][crc_hi]."""

    def can_parse(self, raw: bytes) -> bool:
        return len(raw) >= 4

    def parse(self, raw: bytes) -> ParsedMessage:
        if not self.can_parse(raw):
            raise ValueError("frame Modbus RTU invalido: muy corto")
        address = raw[0]
        function_code = raw[1]
        data = raw[2:-2]
        crc = raw[-2:]
        return ParsedMessage(
            protocol="modbus_rtu",
            payload={
                "address": address,
                "function_code": function_code,
                "data": data.hex(),
                "crc": crc.hex(),
            },
        )


class NMEAParser(MessageParser):
    """Parsea sentencias NMEA tipo $GPGGA,campo1,campo2,...*checksum."""

    def can_parse(self, raw: bytes) -> bool:
        texto = raw.decode("ascii", errors="ignore")
        return texto.startswith("$") and "*" in texto

    def parse(self, raw: bytes) -> ParsedMessage:
        if not self.can_parse(raw):
            raise ValueError("sentencia NMEA invalida")
        texto = raw.decode("ascii").strip()
        cuerpo, checksum = texto[1:].split("*")
        campos = cuerpo.split(",")
        return ParsedMessage(
            protocol="nmea",
            payload={"tipo": campos[0], "campos": campos[1:], "checksum": checksum},
        )
