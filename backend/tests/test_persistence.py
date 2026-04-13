"""Persistence tests for the SQLite-backed workload store."""

from __future__ import annotations

from app.data.workloads import WORKLOADS
from app.store.workloads import WorkloadStore, workload_store


def test_store_survives_reinstantiation() -> None:
    """A fresh WorkloadStore should see rows created by the singleton."""
    created = workload_store.create(
        agent="Persistence Test",
        summary="잔존 여부 확인용",
    )
    assert created.status == "running"

    # New instance points at the same DB path (set by conftest).
    fresh = WorkloadStore()
    found = fresh.get(created.id)
    assert found is not None
    assert found.agent == "Persistence Test"
    assert found.status == "running"


def test_reset_restores_seed() -> None:
    workload_store.create(agent="Temp", summary="곧 사라질 작업")
    assert len(workload_store.list()) == len(WORKLOADS) + 1

    workload_store.reset(WORKLOADS)
    assert len(workload_store.list()) == len(WORKLOADS)
    assert all(w.agent != "Temp" for w in workload_store.list())


def test_create_allocates_monotonic_ids() -> None:
    first = workload_store.create(agent="Seq A", summary="1")
    second = workload_store.create(agent="Seq B", summary="2")

    first_num = int(first.id.split("-")[1])
    second_num = int(second.id.split("-")[1])
    assert second_num == first_num + 1


def test_update_status_round_trip() -> None:
    wl = workload_store.create(agent="Updatable", summary="initial")
    updated = workload_store.update_status(
        wl.id,
        status="success",
        duration_sec=7,
        summary="done",
    )
    assert updated is not None
    assert updated.status == "success"
    assert updated.duration_sec == 7
    assert updated.summary == "done"
