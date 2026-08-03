from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .storage import WorkspaceStore


@dataclass(frozen=True)
class Finding:
    module: str; host: str; port: int | None; severity: str
    title: str; evidence: str; remediation: str


def _cleartext(rows) -> list[Finding]:
    risky = {21: "FTP", 23: "Telnet", 80: "HTTP", 110: "POP3", 143: "IMAP"}
    return [Finding("cleartext-services", r["host"], r["port"], "medium",
        f"Serviço {risky[r['port']]} potencialmente sem criptografia",
        f"Nmap reportou {r['protocol']}/{r['port']} aberto ({r['name'] or 'serviço desconhecido'}).",
        "Prefira uma variante protegida por TLS/SSH ou restrinja o acesso à rede de gestão.")
        for r in rows if r["state"] == "open" and r["port"] in risky]


def _admin(rows) -> list[Finding]:
    ports = {22, 3389, 5900, 5985}
    return [Finding("management-exposure", r["host"], r["port"], "low",
        "Interface de administração exposta", f"Porta de gestão {r['port']}/{r['protocol']} aparece aberta.",
        "Limite a origem com firewall/VPN e aplique autenticação forte.")
        for r in rows if r["state"] == "open" and r["port"] in ports]


def _unknown(rows) -> list[Finding]:
    return [Finding("service-identification", r["host"], r["port"], "info",
        "Serviço aberto sem identificação", f"Nmap não identificou o serviço em {r['port']}/{r['protocol']}.",
        "Confirme a finalidade do serviço e documente seu proprietário.")
        for r in rows if r["state"] == "open" and not r["name"]]


MODULES: dict[str, tuple[str, Callable]] = {
    "cleartext-services": ("Sinaliza protocolos possivelmente sem criptografia.", _cleartext),
    "management-exposure": ("Revisa a exposição de portas comuns de administração.", _admin),
    "service-identification": ("Localiza serviços abertos não identificados.", _unknown),
}


def run_modules(store: WorkspaceStore, names: list[str]) -> int:
    selected = list(MODULES) if names == ["all"] else names
    unknown = set(selected) - set(MODULES)
    if unknown:
        raise ValueError(f"módulo desconhecido: {', '.join(sorted(unknown))}")
    total = 0
    with store.connect() as db:
        rows = db.execute("SELECT * FROM services ORDER BY host, port").fetchall()
        for name in selected:
            for f in MODULES[name][1](rows):
                db.execute("""INSERT OR REPLACE INTO findings
                    (module,host,port,severity,title,evidence,remediation) VALUES (?,?,?,?,?,?,?)""",
                    (f.module, f.host, f.port, f.severity, f.title, f.evidence, f.remediation))
                total += 1
    return total

