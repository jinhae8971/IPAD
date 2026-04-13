"""In-memory workload store.

Phase 7 uses a process-local dict. A later phase will back this with
SQLite so state survives restarts and can be queried from multiple
workers.
"""

from __future__ import annotations

import itertools
from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import Iterable

from ..models import Workload, WorkloadStatus

KST = timezone(timedelta(hours=9))


def _now_kst() -> str:
    return datetime.now(KST).strftime("%Y-%m-%d %H:%M KST")


class WorkloadStore:
    """Thread-safe workload registry."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._items: dict[str, Workload] = {}
        self._counter = itertools.count(200)

    def seed(self, workloads: Iterable[Workload]) -> None:
        with self._lock:
            for w in workloads:
                self._items[w.id] = w

    def list(self) -> list[Workload]:
        with self._lock:
            # Newest first by id (lexicographic is fine for wl-NNNN)
            return sorted(self._items.values(), key=lambda w: w.id, reverse=True)

    def get(self, workload_id: str) -> Workload | None:
        with self._lock:
            return self._items.get(workload_id)

    def create(self, *, agent: str, summary: str) -> Workload:
        with self._lock:
            wl_id = f"wl-{next(self._counter):04d}"
            workload = Workload(
                id=wl_id,
                agent=agent,
                status="running",
                startedAt=_now_kst(),
                durationSec=0,
                summary=summary,
            )
            self._items[wl_id] = workload
            return workload

    def update_status(
        self,
        workload_id: str,
        *,
        status: WorkloadStatus,
        duration_sec: int,
        summary: str | None = None,
    ) -> Workload | None:
        with self._lock:
            existing = self._items.get(workload_id)
            if existing is None:
                return None
            updated = existing.model_copy(
                update={
                    "status": status,
                    "duration_sec": duration_sec,
                    "summary": summary if summary is not None else existing.summary,
                }
            )
            self._items[workload_id] = updated
            return updated


# Module-level singleton pre-seeded with sample workloads so the
# workloads tab looks populated before any real run happens.
from ..data.workloads import WORKLOADS as _SEED_WORKLOADS  # noqa: E402

workload_store = WorkloadStore()
workload_store.seed(_SEED_WORKLOADS)
