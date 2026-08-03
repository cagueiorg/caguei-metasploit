from __future__ import annotations

import html
import json
from pathlib import Path

from .storage import WorkspaceStore


def generate(store: WorkspaceStore, output: Path, fmt: str) -> int:
    with store.connect() as db:
        hosts = [dict(r) for r in db.execute("SELECT * FROM hosts ORDER BY address")]
        services = [dict(r) for r in db.execute("SELECT * FROM services ORDER BY host,port")]
        findings = [dict(r) for r in db.execute("SELECT * FROM findings ORDER BY host,port")]
    data = {"project": "caguei metasploit", "hosts": hosts, "services": services, "findings": findings,
            "notice": "Relatório defensivo baseado somente em dados importados."}
    output.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "json":
        text = json.dumps(data, indent=2, ensure_ascii=False)
    else:
        lines = ["# Relatório — caguei metasploit", "", data["notice"], "", f"Hosts: {len(hosts)} | Serviços: {len(services)} | Achados: {len(findings)}", "", "## Achados", ""]
        lines += [f"### [{f['severity'].upper()}] {f['title']}\n\n- Alvo: `{f['host']}:{f['port'] or '-'}`\n- Evidência: {f['evidence']}\n- Recomendação: {f['remediation']}\n" for f in findings]
        markdown = "\n".join(lines)
        text = markdown if fmt == "md" else f"<!doctype html><meta charset='utf-8'><title>Relatório</title><style>body{{font:16px system-ui;max-width:900px;margin:40px auto}}pre{{white-space:pre-wrap}}</style><pre>{html.escape(markdown)}</pre>"
    output.write_text(text, encoding="utf-8")
    return len(findings)
