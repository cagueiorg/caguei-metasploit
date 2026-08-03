from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .modules import MODULES, run_modules
from .nmap_import import import_nmap
from .report import generate
from .scope import ScopeError, acknowledgement, load_scope
from .storage import WorkspaceStore


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cmsp", description="Auditoria defensiva offline para laboratórios autorizados")
    p.add_argument("--data-dir", type=Path, default=Path(os.getenv("CMSP_HOME", ".cmsp")))
    sub = p.add_subparsers(dest="command", required=True)
    ws = sub.add_parser("workspace", help="gerenciar workspaces"); wsub = ws.add_subparsers(dest="action", required=True)
    wc = wsub.add_parser("create"); wc.add_argument("name")
    wsub.add_parser("list")
    ack = sub.add_parser("scope-ack", help="calcular a confirmação para um scope"); ack.add_argument("scope", type=Path)
    imp = sub.add_parser("import-nmap"); imp.add_argument("workspace"); imp.add_argument("xml", type=Path); imp.add_argument("--scope", type=Path, required=True); imp.add_argument("--ack", required=True)
    mod = sub.add_parser("modules"); mod.add_subparsers(dest="action", required=True).add_parser("list")
    audit = sub.add_parser("audit"); audit.add_argument("workspace"); audit.add_argument("modules", nargs="+", metavar="MODULE"); audit.add_argument("--scope", type=Path, required=True); audit.add_argument("--ack", required=True)
    rep = sub.add_parser("report"); rep.add_argument("workspace"); rep.add_argument("--scope", type=Path, required=True); rep.add_argument("--ack", required=True); rep.add_argument("--format", choices=["json", "md", "html"], default="md"); rep.add_argument("--output", type=Path, required=True)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "workspace" and args.action == "create":
            WorkspaceStore(args.data_dir, args.name).create(); print(f"workspace criado: {args.name}"); return 0
        if args.command == "workspace" and args.action == "list":
            if args.data_dir.exists():
                print("\n".join(sorted(p.name for p in args.data_dir.iterdir() if (p / "workspace.db").exists())))
            return 0
        if args.command == "scope-ack":
            scope = load_scope(args.scope); print(acknowledgement(scope.authorization)); return 0
        if args.command == "modules":
            for name, (description, _) in MODULES.items(): print(f"{name:24} {description}")
            return 0
        scope = load_scope(args.scope, args.ack)
        store = WorkspaceStore(args.data_dir, args.workspace)
        if args.command == "import-nmap":
            h, s, skipped = import_nmap(args.xml, store, scope); print(f"importados: {h} hosts, {s} serviços; fora do scope: {skipped}")
        elif args.command == "audit":
            print(f"achados registrados: {run_modules(store, args.modules)}")
        elif args.command == "report":
            count = generate(store, args.output, args.format); print(f"relatório criado: {args.output} ({count} achados)")
        return 0
    except (FileExistsError, FileNotFoundError, ScopeError, ValueError) as exc:
        print(f"erro: {exc}", file=sys.stderr); return 2


if __name__ == "__main__":
    raise SystemExit(main())

