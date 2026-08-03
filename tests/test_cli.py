from caguei_metasploit.cli import main


def test_module_catalog(capsys):
    assert main(["modules", "list"]) == 0
    assert "cleartext-services" in capsys.readouterr().out


def test_banner(capsys):
    assert main(["banner"]) == 0
    output = capsys.readouterr().out
    assert "auditoria defensiva" in output
