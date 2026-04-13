"""Doc Summarizer agent.

Given a body of text, produces a short structured summary plus a list
of key quotes. Uses prompt caching on the system preamble.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass

from ..llm.client import LLMClient, create_llm_client
from ..store.workloads import workload_store

DEFAULT_MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """You are Doc Summarizer, an agent that condenses long documents into
structured notes. Always respond with STRICT JSON matching this schema:

{
  "summary": "2-4 sentence summary",
  "quotes": ["most impactful quote", "second most impactful quote"]
}

Rules:
- Preserve the document's original language in summary and quotes.
- Keep the summary under ~80 words.
- Return at most 3 quotes, each under 25 words.
- Do not include any text outside the JSON object.
"""


class SummarizerError(RuntimeError):
    """Raised when the LLM call or its response cannot be processed."""


@dataclass
class SummaryResult:
    summary: str
    quotes: list[str]
    model: str
    input_tokens: int
    output_tokens: int
    workload_id: str
    duration_sec: int


def _extract_json(text: str) -> dict:
    """Parse the first JSON object out of the model's reply."""
    # Fast path: whole reply is JSON.
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match is None:
        raise SummarizerError("Model response did not contain a JSON object")
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        raise SummarizerError(f"Model response was not valid JSON: {exc}") from exc


def summarize(
    text: str,
    *,
    client: LLMClient | None = None,
    model: str = DEFAULT_MODEL,
) -> SummaryResult:
    """Run the Doc Summarizer and record a workload entry."""
    if not text.strip():
        raise ValueError("text must not be empty")

    llm = client or create_llm_client()
    workload = workload_store.create(
        agent="Doc Summarizer",
        summary=f"요약 생성 중: {text[:40]}...",
    )
    started = time.monotonic()

    try:
        result = llm.complete(
            system=SYSTEM_PROMPT,
            user=text,
            model=model,
            max_tokens=600,
        )
        parsed = _extract_json(result.text)
        summary_text = str(parsed.get("summary", "")).strip()
        quotes_raw = parsed.get("quotes", [])
        quotes = [str(q).strip() for q in quotes_raw if str(q).strip()]
        if not summary_text:
            raise SummarizerError("Model returned empty summary")

        duration = int(time.monotonic() - started)
        result_payload = {
            "input_preview": text[:500],
            "summary": summary_text,
            "quotes": quotes[:3],
            "model": result.model,
            "input_tokens": result.input_tokens,
            "output_tokens": result.output_tokens,
        }
        workload_store.update_status(
            workload.id,
            status="success",
            duration_sec=duration,
            summary=f"요약 완료: {summary_text[:60]}",
            result=result_payload,
        )
        return SummaryResult(
            summary=summary_text,
            quotes=quotes[:3],
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
