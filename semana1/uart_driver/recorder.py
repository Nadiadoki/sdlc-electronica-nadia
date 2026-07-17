"""
recorder.py — SRP.
Única responsabilidad: persistir mensajes ya parseados como JSON-lines.
No lee del puerto, no parsea: solo guarda.
"""
import json
from pathlib import Path

from parsers import ParsedMessage


class DataRecorder:
    def __init__(self, path: str) -> None:
        self._path = Path(path)

    def record(self, message: ParsedMessage) -> None:
        linea = json.dumps({"protocol": message.protocol, "payload": message.payload})
        with open(self._path, "a") as f:
            f.write(linea + "\n")
