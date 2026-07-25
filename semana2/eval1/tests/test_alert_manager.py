from alerts import ConsoleAlert


def test_console_alert_imprime_el_mensaje(capsys):
    alert = ConsoleAlert()
    alert.send("Anomalia en TEMP-01: 40.0")
    salida = capsys.readouterr().out
    assert "Anomalia en TEMP-01: 40.0" in salida


def test_file_alert_escribe_en_archivo(tmp_path):
    from alerts import FileAlert

    path = tmp_path / "alertas.log"
    alert = FileAlert(path=str(path))
    alert.send("Anomalia en HUM-02: 88.0")
    assert "Anomalia en HUM-02: 88.0" in path.read_text()