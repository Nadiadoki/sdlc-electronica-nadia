from abc import ABC, abstractmethod


class AlertStrategy(ABC):
    """Estrategia abstracta: cualquier forma de enviar una alerta implementa esto."""

    @abstractmethod
    def send(self, message: str) -> None: ...


class ConsoleAlert(AlertStrategy):
    def send(self, message: str) -> None:
        print(message)


class FileAlert(AlertStrategy):
    def __init__(self, path: str) -> None:
        self._path = path

    def send(self, message: str) -> None:
        with open(self._path, "a") as f:
            f.write(message + "\n")