"""SQLite persistence for the AI Workstation backend.

A tiny wrapper around :mod:`sqlite3` that creates the schema on first
use and yields short-lived connections. The store layer is the only
consumer; routers and agents never touch SQL directly.

The DB path is taken from ``WORKSTATION_DB_PATH`` when set, otherwise
``backend/data/workstation.db`` (so local dev just works). Tests set
the env var to a temp file in conftest.
"""

from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

_DEFAULT_PATH = Path(__file__).resolve().parent.parent / "data" / "workstation.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS workloads (
    id TEXT PRIMARY KEY,
    agent TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TEXT NOT NULL,
    duration_sec INTEGER NOT NULL,
    summary TEXT NOT NULL,
    result_json TEXT
);
CREATE INDEX IF NOT EXISTS idx_workloads_id_desc ON workloads(id DESC);
"""


def _ensure_columns(conn) -> None:  # noqa: ANN001
    """Idempotent column migrations.

    SQLite's ``CREATE TABLE IF NOT EXISTS`` cannot add columns to an
    existing table, so we explicitly ALTER when we ship a new field.
    Each ALTER is wrapped in try/except OperationalError so reruns are
    safe.
    """
    cols = {row[1] for row in conn.execute("PRAGMA table_info(workloads)").fetchall()}
    if "result_json" not in cols:
        conn.execute("ALTER TABLE workloads ADD COLUMN result_json TEXT")


def get_db_path() -> Path:
    env = os.environ.get("WORKSTATION_DB_PATH")
    return Path(env) if env else _DEFAULT_PATH


@contextmanager
def get_conn() -> Iterator[sqlite3.Connection]:
    path = get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_schema() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA)
        _ensure_columns(conn)
