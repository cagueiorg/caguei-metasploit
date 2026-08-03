from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS hosts (
  address TEXT PRIMARY KEY, hostname TEXT, state TEXT NOT NULL, imported_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS services (
  host TEXT NOT NULL, port INTEGER NOT NULL, protocol TEXT NOT NULL,
  state TEXT NOT NULL, name TEXT, product TEXT, version TEXT,
  PRIMARY KEY(host, port, protocol), FOREIGN KEY(host) REFERENCES hosts(address)
);
CREATE TABLE IF NOT EXISTS findings (
  id INTEGER PRIMARY KEY AUTOINCREMENT, module TEXT NOT NULL, host TEXT NOT NULL,
  port INTEGER, severity TEXT NOT NULL, title TEXT NOT NULL, evidence TEXT NOT NULL,
  remediation TEXT NOT NULL, UNIQUE(module, host, port, title)
);
"""


class WorkspaceStore:
    def __init__(self, root: Path, name: str):
        self.path = root / name
        self.db_path = self.path / "workspace.db"

    def create(self) -> None:
        self.path.mkdir(parents=True, exist_ok=False)
        (self.path / "scope.example.json").write_text(json.dumps({
            "authorized_use_only": True,
            "authorization": "laboratorio interno autorizado",
            "networks": ["192.0.2.0/24"], "hosts": []
        }, indent=2), encoding="utf-8")
        with self.connect() as db:
            db.executescript(SCHEMA)

    @contextmanager
    def connect(self):
        if not self.path.exists():
            raise FileNotFoundError(f"workspace inexistente: {self.path.name}")
        db = sqlite3.connect(self.db_path)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        db.executescript(SCHEMA)
        try:
            yield db
            db.commit()
        finally:
            db.close()

