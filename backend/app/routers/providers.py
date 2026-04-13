"""Provider endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from ..data.providers import PROVIDERS
from ..models import Provider

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("", response_model=list[Provider])
def list_providers() -> list[Provider]:
    return PROVIDERS
