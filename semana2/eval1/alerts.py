from abc import ABC, abstractmethod


class AlertStrategy(ABC):
    """Estrategia abstracta: cualquier forma de enviar una alerta implementa esto."""

    @abstractmethod
    def send(self, message: str) -> None: ...


class ConsoleAlert(AlertStrategy):
    def send(self, message: str) -> None:
        print(message)