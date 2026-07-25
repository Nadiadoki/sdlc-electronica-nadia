from alert_manager import AlertManager
from anomaly import AnomalyDetector
from sensors import SensorType
from simulator import SensorSimulator


def test_integracion_10_sensores_60_ciclos_dispara_alertas():
    sensor_ids = [f"TEMP-{i:02d}" for i in range(1, 11)]
    simulador = SensorSimulator(
        sensor_ids=sensor_ids,
        sensor_type=SensorType.TEMPERATURE,
        mean=30.0,
        stddev=6.0,
        seed=123,
    )
    detector = AnomalyDetector(threshold=35.0)

    mensajes = []

    class AlertaDePrueba:
        def send(self, message: str) -> None:
            mensajes.append(message)

    manager = AlertManager(detector=detector, alert=AlertaDePrueba())

    total_lecturas = 0
    for _ in range(60):
        for lectura in simulador.generate_cycle():
            manager.process(lectura)
            total_lecturas += 1

    assert total_lecturas == 10 * 60
    assert len(mensajes) > 0
    assert all("TEMP-" in m for m in mensajes)