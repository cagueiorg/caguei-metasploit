import json
from pathlib import Path

from caguei_metasploit.modules import run_modules
from caguei_metasploit.nmap_import import import_nmap
from caguei_metasploit.report import generate
from caguei_metasploit.scope import load_scope
from caguei_metasploit.storage import WorkspaceStore

XML = """<nmaprun><host><status state="up"/><address addr="192.0.2.10" addrtype="ipv4"/><ports>
<port protocol="tcp" portid="23"><state state="open"/><service name="telnet"/></port>
</ports></host><host><status state="up"/><address addr="198.51.100.1" addrtype="ipv4"/></host></nmaprun>"""


def test_import_audit_report(tmp_path: Path):
    store = WorkspaceStore(tmp_path / "data", "lab"); store.create()
    scope_path = tmp_path / "scope.json"
    scope_path.write_text(json.dumps({"authorized_use_only": True, "authorization": "teste autorizado", "networks": ["192.0.2.0/24"]}))
    xml = tmp_path / "scan.xml"; xml.write_text(XML)
    assert import_nmap(xml, store, load_scope(scope_path)) == (1, 1, 1)
    assert run_modules(store, ["all"]) == 1
    output = tmp_path / "report.json"
    assert generate(store, output, "json") == 1
    assert json.loads(output.read_text())["findings"][0]["module"] == "cleartext-services"
