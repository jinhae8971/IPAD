"""Workload endpoints backed by the in-memory store."""

from __future__ import annotations

from fastapi import APIRouter

from ..models import Workload
from ..store.workloads import workload_store

router = APIRouter(prefix="/workloads", tags=["workloads"])


@router.get("", response_model=list[Workload], response_model_by_alias=True)
def list_workloads() -> list[Workload]:
    return workload_store.list()
