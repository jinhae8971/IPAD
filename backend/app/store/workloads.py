"""SQLite-backed workload store.

Public API matches the previous in-memory implementation so routers
and agents don't change: ``list``, ``get``, ``create``, ``update_status``,
``seed``. A new ``reset`` helper wipes and re-seeds the table for
tests.

IDs follow the existing ``wl-NNNN`` pattern; ``create`` picks the next
number based on the current max so they stay monotonically increasing
even across process restarts.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import Iterable

from ..db import get_conn, init_schema
from ..models import Workload, WorkloadStatus

KST = timezone(timedelta(hours=9))

_ID_RE = re.compile(r"^wl-(\d+)$")


def _now_kst() -> str:
    return datetime.now(KST).strftime("%Y-%m-%d %H:%M KST")


def _row_to_workload(row) -> Workload:  # noqa: ANN001
    return Workload(
        id=row["id"],
        agent=row["agent"],
        status=row["status"],
        startedAt=row["started_at"],
        durationSec=row["duration_sec"],
        summary=row["summary"],
    )


def _parse_id(wl_id: str) -> int:
    match = _ID_RE.match(wl_id)
    return int(match.group(1)) if match else 0


def _insert(conn, workload: Workload) -> None:  # noqa: ANN001
    conn.execute(
        """
        INSERT OR REPLACE INTO workloads
            (id, agent, status, started_at, duration_sec, summary)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            workload.id,
            workload.agent,
            workload.status,
            workload.started_at,
            workload.duration_sec,
            workload.summary,
        ),
    )


class WorkloadStore:
    """Thread-safe workload registry backed by SQLite."""

    def __init__(self) -> None:
        self._lock = Lock()
        init_schema()

    def seed(self, workloads: Iterable[Workload]) -> None:
        """Insert workloads only if the table is empty."""
        with self._lock, get_conn() as conn:
            count = conn.execute("SELECT COUNT(*) FROM workloads").fetchone()[0]
            if count > 0:
                return
            for w in workloads:
                _insert(conn, w)

    def reset(self, workloads: Iterable[Workload]) -> None:
        """Wipe the table and re-seed. Intended for tests."""
        with self._lock, get_conn() as conn:
            conn.execute("DELETE FROM workloads")
            for w in workloads:
                _insert(conn, w)

    def list(self) -> list[Workload]:
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM workloads ORDER BY id DESC"
            ).fetchall()
        return [_row_to_workload(r) for r in rows]

    def get(self, workload_id: str) -> Workload | None:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT * FROM workloads WHERE id = ?",
                (workload_id,),
            ).fetchone()
        return _row_to_workload(row) if row else None

    def create(self, *, agent: str, summary: str) -> Workload:
        with self._lock, get_conn() as conn:
            row = conn.execute("SELECT id FROM workloads ORDER BY id DESC LIMIT 1").fetchone()
            next_num = (_parse_id(row["id"]) + 1) if row else 200
            wl_id = f"wl-{next_num:04d}"
            workload = Workload(
                id=wl_id,
                agent=agent,
                status="running",
                startedAt=_now_kst(),
                durationSec=0,
                summary=summary,
            )
            _insert(conn, workload)
            return workload

    def update_status(
        self,
        workload_id: str,
        *,
        status: WorkloadStatus,
        duration_sec: int,
        summary: str | None = None,
    ) -> Workload | None:
        with self._lock, get_conn() as conn:
            existing = conn.execute(
                "SELECT * FROM workloads WHERE id = ?",
                (workload_id,),
            ).fetchone()
            if existing is None:
                return None
            new_summary = summary if summary is not None else existing["summary"]
            conn.execute(
                """
                UPDATE workloads
                SET status = ?, duration_sec = ?, summary = ?
                WHERE id = ?
                """,
                (status, duration_sec, new_summary, workload_id),
            )
            row = conn.execute(
                "SELECT * FROM workloads WHERE id = ?",
                (workload_id,),
            ).fetchone()
        return _row_to_workload(row) if row else None


# Module-level singleton. ``seed`` is a no-op on subsequent process
# starts because the table already has rows (the Docker volume keeps
# /data/workstation.db around across container restarts).
from ..data.workloads import WORKLOADS as _SEED_WORKLOADS  # noqa: E402

workload_store = WorkloadStore()
workload_store.seed(_SEED_WORKLOADS)
