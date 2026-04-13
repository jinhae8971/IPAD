"""Tests for GET /api/workloads/{id} and agent result persistence."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.agents import code_reviewer as cr_module
from app.agents import doc_summarizer as ds_module
from app.llm.client import LLMResult
from app.main import app
from app.store.workloads import workload_store

client = TestClient(app)


class FakeLLM:
    def __init__(self, reply: str) -> None:
        self.reply = reply

    def complete(self, *, system: str, user: str, model: str, max_tokens: int = 1024) -> LLMResult:
        return LLMResult(text=self.reply, model=model, input_tokens=10, output_tokens=20)


def test_get_workload_by_id_returns_seed_row() -> None:
    seed = workload_store.list()[-1]  # oldest seeded entry
    response = client.get(f"/api/workloads/{seed.id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == seed.id
    # Seed rows have no result attached.
    assert body["result"] is None


def test_get_workload_unknown_returns_404() -> None:
    response = client.get("/api/workloads/wl-9999")
    assert response.status_code == 404


def test_doc_summarizer_persists_result(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        ds_module,
        "create_llm_client",
        lambda: FakeLLM('{"summary": "한 줄 요약", "quotes": ["인용 1"]}'),
    )

    response = client.post("/api/agents/doc-summarizer/run", json={"text": "원문 문서"})
    assert response.status_code == 200
    workload_id = response.json()["workloadId"]

    detail = client.get(f"/api/workloads/{workload_id}")
    assert detail.status_code == 200
    body = detail.json()
    assert body["status"] == "success"
    assert body["result"] is not None
    assert body["result"]["summary"] == "한 줄 요약"
    assert body["result"]["quotes"] == ["인용 1"]
    assert body["result"]["input_preview"] == "원문 문서"


def test_code_reviewer_persists_result(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        cr_module,
        "create_llm_client",
        lambda: FakeLLM(
            '{"summary": "전반적으로 안전", '
            '"comments": [{"file": "a.py", "line": 1, "severity": "info", "message": "ok"}]}'
        ),
    )

    response = client.post(
        "/api/agents/code-reviewer/run",
        json={"diff": "diff --git a/a.py b/a.py", "context": "ctx"},
    )
    assert response.status_code == 200
    workload_id = response.json()["workloadId"]

    detail = client.get(f"/api/workloads/{workload_id}")
    body = detail.json()
    assert body["status"] == "success"
    assert body["result"]["summary"] == "전반적으로 안전"
    assert body["result"]["context"] == "ctx"
    assert len(body["result"]["comments"]) == 1
    assert body["result"]["comments"][0]["file"] == "a.py"


def test_failed_run_persists_no_result(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        ds_module, "create_llm_client", lambda: FakeLLM("not json at all")
    )

    response = client.post("/api/agents/doc-summarizer/run", json={"text": "doc"})
    assert response.status_code == 502

    failed = workload_store.list()[0]
    assert failed.status == "failed"
    assert failed.result is None
