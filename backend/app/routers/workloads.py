"""Workload endpoints backed by the in-memory store."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..models import Workload
from ..store.workloads import workload_store

router = APIRouter(prefix="/workloads", tags=["workloads"])


@router.get("", response_model=list[Workload], response_model_by_alias=True)
def list_workloads() -> list[Workload]:
    return workload_store.list()


@router.get("/{workload_id}", response_model=Workload, response_model_by_alias=True)
def get_workload(workload_id: str) -> Workload:
    workload = workload_store.get(workload_id)
    if workload is None:
        raise HTTPException(status_code=404, detail=f"Unknown workload: {workload_id}")
    return workload
