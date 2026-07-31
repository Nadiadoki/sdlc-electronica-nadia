class SensorNotFoundError(Exception):
    """El sensor solicitado no esta registrado."""


class SensorAlreadyExistsError(Exception):
    """Ya existe un sensor registrado con ese sensor_id."""


class SensorAlreadyInactiveError(Exception):
    """El sensor ya estaba desactivado."""


class ReadingNotFoundError(Exception):
    """La lectura solicitada no existe."""


class ReadingAlreadyInactiveError(Exception):
    """La lectura ya estaba desactivada; no se puede desactivar de nuevo."""
