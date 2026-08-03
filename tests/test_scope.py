import json
from pathlib import Path

import pytest

from caguei_metasploit.scope import ScopeError, acknowledgement, load_scope


def test_scope_guard_accepts_network(tmp_path: Path):
    p = tmp_path / "scope.json"
    p.write_text(json.dumps({"authorized_use_only": True, "authorization": "lab autorizado", "networks": ["10.0.0.0/24"]}))
    ack = acknowledgement("lab autorizado")
    scope = load_scope(p, ack)
    assert scope.contains("10.0.0.7")
    assert not scope.contains("10.0.1.7")


def test_scope_guard_rejects_bad_ack(tmp_path: Path):
    p = tmp_path / "scope.json"
    p.write_text(json.dumps({"authorized_use_only": True, "authorization": "lab autorizado", "hosts": ["lab.local"]}))
    with pytest.raises(ScopeError): load_scope(p, "errado")
