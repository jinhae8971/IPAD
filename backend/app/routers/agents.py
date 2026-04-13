"""Agent catalog endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..data.agents import AGENTS, CATEGORIES, get_agent, get_agents_by_category
from ..models import Agent, AgentCategory

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("/categories", response_model=list[AgentCategory])
def list_categories() -> list[AgentCategory]:
    return CATEGORIES


@router.get("", response_model=list[Agent])
def list_agents(category: str | None = None) -> list[Agent]:
    if category is None:
        return AGENTS
    return get_agents_by_category(category)


@router.get("/{agent_id}", response_model=Agent)
def get_agent_by_id(agent_id: str) -> Agent:
    agent = get_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail=f"Unknown agent: {agent_id}")
    return agent
