from sensors import SensorType
from simulator import SensorSimulator


def test_generate_cycle_produce_una_lectura_por_sensor():
    sensor_ids = ["TEMP-01", "TEMP-02", "TEMP-03"]
    simulador = SensorSimulator(
        sensor_ids=sensor_ids,
        sensor_type=SensorType.TEMPERATURE,
        mean=30.0,
        stddev=5.0,
        seed=42,
    )
    lecturas = simulador.generate_cycle()
    assert len(lecturas) == 3
    assert {l.sensor_id for l in lecturas} == set(sensor_ids)

def test_generate_cycle_produce_al_menos_una_anomalia_en_muchos_ciclos():
    from anomaly import AnomalyDetector

    simulador = SensorSimulator(
        sensor_ids=["TEMP-01"],
        sensor_type=SensorType.TEMPERATURE,
        mean=30.0,
        stddev=5.0,
        seed=7,
    )
    detector = AnomalyDetector(threshold=35.0)

    anomalias = 0
    for _ in range(100):
        for lectura in simulador.generate_cycle():
            if detector.is_anomaly(lectura):
                anomalias += 1

    assert anomalias > 0