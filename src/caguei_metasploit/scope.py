from __future__ import annotations

import hashlib
import ipaddress
import json
from dataclasses import dataclass
from pathlib import Path


class ScopeError(ValueError):
    pass


@dataclass(frozen=True)
class Scope:
    networks: tuple[ipaddress.IPv4Network | ipaddress.IPv6Network, ...]
    hosts: frozenset[str]
    authorization: str

    def contains(self, address: str) -> bool:
        try:
            ip = ipaddress.ip_address(address)
        except ValueError:
            return address.lower().rstrip(".") in self.hosts
        return any(ip in network for network in self.networks)


def acknowledgement(authorization: str) -> str:
    digest = hashlib.sha256(authorization.strip().encode()).hexdigest()[:12]
    return f"AUTORIZADO-{digest}"


def load_scope(path: Path, supplied_ack: str | None = None) -> Scope:
    if not path.exists():
        raise ScopeError(f"scope obrigatório não encontrado: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise ScopeError(f"scope inválido: {exc}") from exc
    authorization = str(data.get("authorization", "")).strip()
    if len(authorization) < 8:
        raise ScopeError("descreva a autorização no scope (mínimo de 8 caracteres)")
    if data.get("authorized_use_only") is not True:
        raise ScopeError("authorized_use_only deve ser true")
    try:
        networks = tuple(ipaddress.ip_network(item, strict=False) for item in data.get("networks", []))
    except ValueError as exc:
        raise ScopeError(f"rede inválida: {exc}") from exc
    hosts = frozenset(str(item).lower().rstrip(".") for item in data.get("hosts", []))
    if not networks and not hosts:
        raise ScopeError("scope deve conter ao menos uma rede ou host")
    expected = acknowledgement(authorization)
    if supplied_ack is not None and supplied_ack != expected:
        raise ScopeError("confirmação de autorização incorreta")
    return Scope(networks, hosts, authorization)

