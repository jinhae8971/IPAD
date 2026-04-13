"""Thin wrapper around the Anthropic Python SDK.

Agents depend on the ``LLMClient`` protocol, not on the SDK directly,
so tests can monkey-patch ``create_llm_client`` with a fake. Prompt
caching (``cache_control``) is applied to the system prompt so that
repeated calls with the same agent preamble reuse tokens.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol


@dataclass
class LLMResult:
    text: str
    model: str
    input_tokens: int
    output_tokens: int


class LLMClient(Protocol):
    def complete(
        self,
        *,
        system: str,
        user: str,
        model: str,
        max_tokens: int = 1024,
    ) -> LLMResult: ...


class AnthropicClient:
    """Production LLMClient that calls the Anthropic Messages API."""

    def __init__(self, api_key: str | None = None) -> None:
        # Import lazily so missing SDK doesn't break test collection.
        from anthropic import Anthropic  # type: ignore

        self._client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY", ""))

    def complete(
        self,
        *,
        system: str,
        user: str,
        model: str,
        max_tokens: int = 1024,
    ) -> LLMResult:
        response = self._client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=[
                {
                    "type": "text",
                    "text": system,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": user}],
        )
        text = "".join(block.text for block in response.content if getattr(block, "text", None))
        return LLMResult(
            text=text,
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )


def create_llm_client() -> LLMClient:
    """Factory used by agents; tests monkey-patch this symbol."""
    return AnthropicClient()
