from caguei_metasploit.cli import main


def test_module_catalog(capsys):
    assert main(["modules", "list"]) == 0
    assert "cleartext-services" in capsys.readouterr().out
