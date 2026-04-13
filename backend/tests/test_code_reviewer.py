"""Tests for the Code Reviewer agent endpoint.

LLM calls are always mocked; the Anthropic SDK is never reached.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.agents import code_reviewer as cr_module
from app.llm.client import LLMResult
from app.main import app
from app.store.workloads import workload_store

client = TestClient(app)


SAMPLE_DIFF = """diff --git a/src/foo.py b/src/foo.py
--- a/src/foo.py
+++ b/src/foo.py
@@ -10,7 +10,7 @@ def compute(total):
-    return total / count
+    return total // count
"""


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
            input_tokens=321,
            output_tokens=64,
        )


@pytest.fixture
def fake_llm(monkeypatch: pytest.MonkeyPatch) -> FakeLLM:
    fake = FakeLLM(
        reply=(
            '{"summary": "대체로 안전한 변경입니다.", '
            '"comments": ['
            '{"file": "src/foo.py", "line": 12, "severity": "warning", '
            '"message": "0으로 나누기 위험이 남아있습니다"}, '
            '{"file": "src/foo.py", "line": 12, "severity": "critical", '
            '"message": "count가 0일 때 ZeroDivisionError 발생"}'
            ']}'
        )
    )
    monkeypatch.setattr(cr_module, "create_llm_client", lambda: fake)
    return fake


def test_run_code_reviewer_success(fake_llm: FakeLLM) -> None:
    before = len(workload_store.list())

    response = client.post(
        "/api/agents/code-reviewer/run",
        json={"diff": SAMPLE_DIFF},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["summary"] == "대체로 안전한 변경입니다."
    assert len(body["comments"]) == 2
    # Critical should come first after severity sort.
    assert body["comments"][0]["severity"] == "critical"
    assert body["comments"][1]["severity"] == "warning"
    assert body["inputTokens"] == 321
    assert body["outputTokens"] == 64
    assert body["workloadId"].startswith("wl-")

    assert len(fake_llm.calls) == 1
    call = fake_llm.calls[0]
    assert "Code Reviewer" in call["system"]
    assert "src/foo.py" in call["user"]

    after = workload_store.list()
    assert len(after) == before + 1
    created = next(w for w in after if w.id == body["workloadId"])
    assert created.status == "success"
    assert created.agent == "Code Reviewer"


def test_run_code_reviewer_forwards_context(fake_llm: FakeLLM) -> None:
    response = client.post(
        "/api/agents/code-reviewer/run",
        json={"diff": SAMPLE_DIFF, "context": "Release blocker candidate"},
    )
    assert response.status_code == 200
    user_payload = fake_llm.calls[0]["user"]
    assert "Release blocker candidate" in user_payload
    assert "src/foo.py" in user_payload


def test_run_code_reviewer_rejects_empty_diff() -> None:
    response = client.post("/api/agents/code-reviewer/run", json={"diff": ""})
    assert response.status_code == 422


def test_run_code_reviewer_marks_failed_on_bad_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bad = FakeLLM(reply="no json here")
    monkeypatch.setattr(cr_module, "create_llm_client", lambda: bad)

    response = client.post(
        "/api/agents/code-reviewer/run",
        json={"diff": SAMPLE_DIFF},
    )
    assert response.status_code == 502

    latest = workload_store.list()[0]
    assert latest.agent == "Code Reviewer"
    assert latest.status == "failed"
