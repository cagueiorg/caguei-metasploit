from __future__ import annotations

import datetime as dt
import xml.etree.ElementTree as ET
from pathlib import Path

from .scope import Scope, ScopeError
from .storage import WorkspaceStore


def import_nmap(path: Path, store: WorkspaceStore, scope: Scope) -> tuple[int, int, int]:
    """Import Nmap XML without executing Nmap or touching the network."""
    try:
        if path.stat().st_size > 20 * 1024 * 1024:
            raise ValueError("XML excede o limite seguro de 20 MiB")
    except OSError as exc:
        raise ValueError(f"não foi possível ler o XML: {exc}") from exc
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        raise ValueError(f"XML Nmap inválido: {exc}") from exc
    if root.tag != "nmaprun":
        raise ValueError("arquivo não parece ser um Nmap XML")
    imported = skipped = services = 0
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    with store.connect() as db:
        for node in root.findall("host"):
            addr_node = node.find("address")
            if addr_node is None or not addr_node.get("addr"):
                continue
            address = addr_node.get("addr", "")
            hostname_node = node.find("hostnames/hostname")
            hostname = hostname_node.get("name", "") if hostname_node is not None else ""
            if not (scope.contains(address) or (hostname and scope.contains(hostname))):
                skipped += 1
                continue
            state_node = node.find("status")
            state = state_node.get("state", "unknown") if state_node is not None else "unknown"
            db.execute("INSERT OR REPLACE INTO hosts VALUES (?, ?, ?, ?)", (address, hostname, state, now))
            imported += 1
            for port in node.findall("ports/port"):
                state_el, service_el = port.find("state"), port.find("service")
                values = (
                    address, int(port.get("portid", "0")), port.get("protocol", "tcp"),
                    state_el.get("state", "unknown") if state_el is not None else "unknown",
                    service_el.get("name", "") if service_el is not None else "",
                    service_el.get("product", "") if service_el is not None else "",
                    service_el.get("version", "") if service_el is not None else "",
                )
                db.execute("INSERT OR REPLACE INTO services VALUES (?, ?, ?, ?, ?, ?, ?)", values)
                services += 1
    if imported == 0 and skipped:
        raise ScopeError("nenhum host importado: todos estão fora do scope")
    return imported, services, skipped
