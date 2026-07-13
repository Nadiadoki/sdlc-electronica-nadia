from hola_sensor import Sensor


def test_read_devuelve_23_5():
    sensor = Sensor()
    assert sensor.read() == 23.5