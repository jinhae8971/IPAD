"""Agent catalog + run endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..agents.code_reviewer import CodeReviewerError, review
from ..agents.doc_summarizer import SummarizerError, summarize
from ..data.agents import AGENTS, CATEGORIES, get_agent, get_agents_by_category
from ..models import (
    Agent,
    AgentCategory,
    CodeReviewComment,
    CodeReviewerRequest,
    CodeReviewerResponse,
    DocSummarizerRequest,
    DocSummarizerResponse,
)

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


@router.post(
    "/doc-summarizer/run",
    response_model=DocSummarizerResponse,
    response_model_by_alias=True,
)
def run_doc_summarizer(request: DocSummarizerRequest) -> DocSummarizerResponse:
    try:
        result = summarize(request.text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except SummarizerError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"LLM call failed: {exc}") from exc

    return DocSummarizerResponse(
        summary=result.summary,
        quotes=result.quotes,
        model=result.model,
        inputTokens=result.input_tokens,
        outputTokens=result.output_tokens,
        workloadId=result.workload_id,
        durationSec=result.duration_sec,
    )


@router.post(
    "/code-reviewer/run",
    response_model=CodeReviewerResponse,
    response_model_by_alias=True,
)
def run_code_reviewer(request: CodeReviewerRequest) -> CodeReviewerResponse:
    try:
        result = review(request.diff, context=request.context)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except CodeReviewerError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"LLM call failed: {exc}") from exc

    return CodeReviewerResponse(
        summary=result.summary,
        comments=[
            CodeReviewComment(
                file=c.file,
                line=c.line,
                severity=c.severity,
                message=c.message,
            )
            for c in result.comments
        ],
        model=result.model,
        inputTokens=result.input_tokens,
        outputTokens=result.output_tokens,
        workloadId=result.workload_id,
        durationSec=result.duration_sec,
    )
