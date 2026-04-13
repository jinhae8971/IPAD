"""Code Reviewer agent.

Given a unified diff (and optional surrounding context), produces a
list of review comments with severity levels and a short high-level
summary. Uses prompt caching on the system preamble and records a
workload entry through the shared store.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from typing import Literal

from ..llm.client import LLMClient, create_llm_client
from ..store.workloads import workload_store

DEFAULT_MODEL = "claude-sonnet-4-6"

Severity = Literal["info", "warning", "critical"]

SYSTEM_PROMPT = """You are Code Reviewer, an agent that reviews unified diffs and
returns actionable feedback. Always respond with STRICT JSON matching this
schema:

{
  "summary": "1-2 sentence overall take on the change",
  "comments": [
    {
      "file": "path/to/file",
      "line": 42,
      "severity": "info" | "warning" | "critical",
      "message": "short explanation of the concern and a suggested fix"
    }
  ]
}

Rules:
- Preserve the language of the diff author's comments.
- Keep the summary under ~40 words.
- Return at most 8 comments, ordered by severity (critical first).
- ``line`` is the 1-based line number in the NEW version of the file.
- Use "critical" only for bugs, correctness issues, or security concerns.
- Do not include any text outside the JSON object.
"""


class CodeReviewerError(RuntimeError):
    """Raised when the LLM call or its response cannot be processed."""


@dataclass
class ReviewComment:
    file: str
    line: int
    severity: Severity
    message: str


@dataclass
class ReviewResult:
    summary: str
    comments: list[ReviewComment]
    model: str
    input_tokens: int
    output_tokens: int
    workload_id: str
    duration_sec: int


def _extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match is None:
        raise CodeReviewerError("Model response did not contain a JSON object")
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        raise CodeReviewerError(f"Model response was not valid JSON: {exc}") from exc


def _normalize_comments(raw: object) -> list[ReviewComment]:
    if not isinstance(raw, list):
        return []
    comments: list[ReviewComment] = []
    for item in raw[:8]:
        if not isinstance(item, dict):
            continue
        severity = str(item.get("severity", "info"))
        if severity not in ("info", "warning", "critical"):
            severity = "info"
        try:
            line = int(item.get("line", 0))
        except (TypeError, ValueError):
            line = 0
        comments.append(
            ReviewComment(
                file=str(item.get("file", "")).strip(),
                line=line,
                severity=severity,  # type: ignore[arg-type]
                message=str(item.get("message", "")).strip(),
            )
        )
    severity_order = {"critical": 0, "warning": 1, "info": 2}
    comments.sort(key=lambda c: severity_order.get(c.severity, 3))
    return comments


def review(
    diff: str,
    *,
    context: str | None = None,
    client: LLMClient | None = None,
    model: str = DEFAULT_MODEL,
) -> ReviewResult:
    """Run the Code Reviewer and record a workload entry."""
    if not diff.strip():
        raise ValueError("diff must not be empty")

    llm = client or create_llm_client()
    preview = diff.strip().splitlines()[0][:50] if diff.strip() else ""
    workload = workload_store.create(
        agent="Code Reviewer",
        summary=f"리뷰 생성 중: {preview}",
    )
    started = time.monotonic()

    user = diff if context is None else f"CONTEXT:\n{context}\n\nDIFF:\n{diff}"

    try:
        result = llm.complete(
            system=SYSTEM_PROMPT,
            user=user,
            model=model,
            max_tokens=1200,
        )
        parsed = _extract_json(result.text)
        summary_text = str(parsed.get("summary", "")).strip()
        if not summary_text:
            raise CodeReviewerError("Model returned empty summary")
        comments = _normalize_comments(parsed.get("comments", []))

        duration = int(time.monotonic() - started)
        workload_store.update_status(
            workload.id,
            status="success",
            duration_sec=duration,
            summary=f"리뷰 완료: {len(comments)}개 코멘트",
        )
        return ReviewResult(
            summary=summary_text,
            comments=comments,
            model=result.model,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            workload_id=workload.id,
            duration_sec=duration,
        )
    except Exception as exc:  # noqa: BLE001
        duration = int(time.monotonic() - started)
        workload_store.update_status(
            workload.id,
            status="failed",
            duration_sec=duration,
            summary=f"실패: {exc}",
        )
        raise
