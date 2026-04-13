"""Pydantic models for the AI Workstation backend.

These mirror the TypeScript types defined in the frontend under
``src/types/agent.ts`` and related files so the two halves stay in
sync. The backend is the source of truth once the frontend is wired
through React Query; the static frontend catalog is only a fallback.
"""

from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field

AgentCategoryId = Literal["coding", "analysis", "automation", "data", "ops"]
ProviderStatus = Literal["사용 가능", "연결 대기", "미설정"]
WorkloadStatus = Literal["running", "queued", "success", "failed"]


class AgentCategory(BaseModel):
    id: AgentCategoryId
    label: str
    description: str
    icon: str


class Agent(BaseModel):
    id: str
    name: str
    category: AgentCategoryId
    tagline: str
    description: str
    capabilities: List[str]
    default_model: str = Field(alias="defaultModel")
    tags: List[str]

    model_config = {"populate_by_name": True}


class Provider(BaseModel):
    id: str
    name: str
    description: str
    env_key: str = Field(alias="envKey")
    status: ProviderStatus
    models: List[str]

    model_config = {"populate_by_name": True}


class Workload(BaseModel):
    id: str
    agent: str
    status: WorkloadStatus
    started_at: str = Field(alias="startedAt")
    duration_sec: int = Field(alias="durationSec")
    summary: str

    model_config = {"populate_by_name": True}


class HealthResponse(BaseModel):
    status: Literal["ok"]
    version: str


class DocSummarizerRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=50_000)


class DocSummarizerResponse(BaseModel):
    summary: str
    quotes: List[str]
    model: str
    input_tokens: int = Field(alias="inputTokens")
    output_tokens: int = Field(alias="outputTokens")
    workload_id: str = Field(alias="workloadId")
    duration_sec: int = Field(alias="durationSec")

    model_config = {"populate_by_name": True}
