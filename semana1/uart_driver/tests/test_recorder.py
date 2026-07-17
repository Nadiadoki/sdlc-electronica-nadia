import json

from parsers import ParsedMessage
from recorder import DataRecorder


def test_record_escribe_json_lines(tmp_path):
    path = tmp_path / "out.jsonl"
    recorder = DataRecorder(str(path))
    recorder.record(ParsedMessage(protocol="modbus_rtu", payload={"address": 1}))
    contenido = path.read_text().strip()
    data = json.loads(contenido)
    assert data["protocol"] == "modbus_rtu"


def test_record_agrega_multiples_lineas(tmp_path):
    path = tmp_path / "out.jsonl"
    recorder = DataRecorder(str(path))
    recorder.record(ParsedMessage(protocol="nmea", payload={"tipo": "GPGGA"}))
    recorder.record(ParsedMessage(protocol="modbus_rtu", payload={"address": 2}))
    lineas = path.read_text().strip().split("\n")
    assert len(lineas) == 2


def test_record_formato_es_json_valido_por_linea(tmp_path):
    path = tmp_path / "out.jsonl"
    recorder = DataRecorder(str(path))
    recorder.record(ParsedMessage(protocol="nmea", payload={"tipo": "GPGGA"}))
    recorder.record(ParsedMessage(protocol="nmea", payload={"tipo": "GPRMC"}))
    for linea in path.read_text().strip().split("\n"):
        json.loads(linea)  # no debe lanzar error
