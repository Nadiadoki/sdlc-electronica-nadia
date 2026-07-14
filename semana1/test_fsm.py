from fsm_demo import TrafficLightFSM, TrafficLightState


def test_estado_inicial_es_red():
    fsm = TrafficLightFSM()
    assert fsm.state == TrafficLightState.RED


def test_transicion_red_a_green():
    fsm = TrafficLightFSM()
    nuevo_estado = fsm.transition()
    assert nuevo_estado == TrafficLightState.GREEN
    assert fsm.state == TrafficLightState.GREEN


def test_ciclo_completo_vuelve_a_red():
    fsm = TrafficLightFSM()
    fsm.transition()  # RED -> GREEN
    fsm.transition()  # GREEN -> YELLOW
    fsm.transition()  # YELLOW -> RED
    assert fsm.state == TrafficLightState.RED


def test_conteo_de_ciclos():
    fsm = TrafficLightFSM()
    assert fsm.cycle_count == 0
    fsm.transition()
    fsm.transition()
    fsm.transition()
    assert fsm.cycle_count == 3
