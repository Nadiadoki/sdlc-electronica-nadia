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