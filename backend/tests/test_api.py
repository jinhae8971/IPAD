"""Smoke tests for the AI Workstation API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_list_categories() -> None:
    response = client.get("/api/agents/categories")
    assert response.status_code == 200
    categories = response.json()
    assert len(categories) == 5
    ids = {c["id"] for c in categories}
    assert ids == {"coding", "analysis", "automation", "data", "ops"}


def test_list_agents_all() -> None:
    response = client.get("/api/agents")
    assert response.status_code == 200
    agents = response.json()
    assert len(agents) == 10
    assert any(a["id"] == "doc-summarizer" for a in agents)
    # Market Analyst belongs to the unrelated analyzer/ project and
    # was removed from the AI Workstation catalog in Phase 12.
    assert all(a["id"] != "market-analyst" for a in agents)


def test_list_agents_filter_by_category() -> None:
    response = client.get("/api/agents", params={"category": "coding"})
    assert response.status_code == 200
    agents = response.json()
    assert len(agents) == 3
    assert {a["id"] for a in agents} == {
        "code-architect",
        "code-implementer",
        "code-reviewer",
    }


def test_get_agent_by_id() -> None:
    response = client.get("/api/agents/code-architect")
    assert response.status_code == 200
    agent = response.json()
    assert agent["name"] == "Code Architect"
    assert "capabilities" in agent
    # Pydantic serializes with alias
    assert "defaultModel" in agent


def test_get_agent_not_found() -> None:
    response = client.get("/api/agents/does-not-exist")
    assert response.status_code == 404


def test_list_providers() -> None:
    response = client.get("/api/providers")
    assert response.status_code == 200
    providers = response.json()
    assert len(providers) == 3
    assert {p["id"] for p in providers} == {"anthropic", "openai", "ollama"}


def test_list_workloads() -> None:
    response = client.get("/api/workloads")
    assert response.status_code == 200
    workloads = response.json()
    assert len(workloads) >= 1
    assert {w["status"] for w in workloads} <= {
        "running",
        "queued",
        "success",
        "failed",
    }
