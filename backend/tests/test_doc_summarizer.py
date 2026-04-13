"""Tests for the Doc Summarizer agent endpoint.

LLM calls are always mocked; the Anthropic SDK is never reached.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.agents import doc_summarizer as ds_module
from app.llm.client import LLMResult
from app.main import app
from app.store.workloads import workload_store

client = TestClient(app)


class FakeLLM:
    def __init__(self, reply: str) -> None:
        self.reply = reply
        self.calls: list[dict] = []

    def complete(self, *, system: str, user: str, model: str, max_tokens: int = 1024) -> LLMResult:
        self.calls.append(
            {"system": system, "user": user, "model": model, "max_tokens": max_tokens}
        )
        return LLMResult(
            text=self.reply,
            model=model,
            input_tokens=123,
            output_tokens=45,
        )


@pytest.fixture
def fake_llm(monkeypatch: pytest.MonkeyPatch) -> FakeLLM:
    fake = FakeLLM(
        reply=(
            '{"summary": "짧은 요약입니다.", '
            '"quotes": ["핵심 인용 1", "핵심 인용 2"]}'
        )
    )
    monkeypatch.setattr(ds_module, "create_llm_client", lambda: fake)
    return fake


def test_run_doc_summarizer_success(fake_llm: FakeLLM) -> None:
    before = len(workload_store.list())

    response = client.post(
        "/api/agents/doc-summarizer/run",
        json={"text": "긴 본문 문서입니다. 여러 문단이 있습니다."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["summary"] == "짧은 요약입니다."
    assert body["quotes"] == ["핵심 인용 1", "핵심 인용 2"]
    assert body["inputTokens"] == 123
    assert body["outputTokens"] == 45
    assert body["workloadId"].startswith("wl-")

    # The fake was actually invoked with the expected system + user.
    assert len(fake_llm.calls) == 1
    call = fake_llm.calls[0]
    assert "Doc Summarizer" in call["system"]
    assert "긴 본문 문서" in call["user"]

    # A new workload was recorded and is now in the list.
    after = workload_store.list()
    assert len(after) == before + 1
    created = next(w for w in after if w.id == body["workloadId"])
    assert created.status == "success"
    assert created.agent == "Doc Summarizer"


def test_run_doc_summarizer_rejects_empty_text() -> None:
    response = client.post("/api/agents/doc-summarizer/run", json={"text": ""})
    # Pydantic min_length=1 rejects empty before reaching the handler.
    assert response.status_code == 422


def test_run_doc_summarizer_marks_workload_failed_on_bad_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bad = FakeLLM(reply="not json at all")
    monkeypatch.setattr(ds_module, "create_llm_client", lambda: bad)

    response = client.post(
        "/api/agents/doc-summarizer/run",
        json={"text": "some document"},
    )
    assert response.status_code == 502

    # The failed workload should still be recorded.
    latest = workload_store.list()[0]
    assert latest.agent == "Doc Summarizer"
    assert latest.status == "failed"


def test_workloads_endpoint_reflects_store(fake_llm: FakeLLM) -> None:
    seed_count = len(workload_store.list())

    client.post(
        "/api/agents/doc-summarizer/run",
        json={"text": "문서 A"},
    )

    response = client.get("/api/workloads")
    assert response.status_code == 200
    workloads = response.json()
    assert len(workloads) == seed_count + 1
    # Newest first.
    assert workloads[0]["agent"] == "Doc Summarizer"
