"""Workload endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from ..data.workloads import WORKLOADS
from ..models import Workload

router = APIRouter(prefix="/workloads", tags=["workloads"])


@router.get("", response_model=list[Workload])
def list_workloads() -> list[Workload]:
    return WORKLOADS
