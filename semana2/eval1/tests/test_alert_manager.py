from alerts import ConsoleAlert


def test_console_alert_imprime_el_mensaje(capsys):
    alert = ConsoleAlert()
    alert.send("Anomalia en TEMP-01: 40.0")
    salida = capsys.readouterr().out
    assert "Anomalia en TEMP-01: 40.0" in salida