"""Seed provider catalog."""

from __future__ import annotations

from ..models import Provider

PROVIDERS: list[Provider] = [
    Provider(
        id="anthropic",
        name="Anthropic",
        description="Claude 4.6 / 4.5 계열. 기본 프로바이더.",
        envKey="ANTHROPIC_API_KEY",
        status="사용 가능",
        models=[
            "claude-opus-4-6",
            "claude-sonnet-4-6",
            "claude-haiku-4-5-20251001",
        ],
    ),
    Provider(
        id="openai",
        name="OpenAI",
        description="GPT 계열. 보조 프로바이더.",
        envKey="OPENAI_API_KEY",
        status="연결 대기",
        models=["gpt-4o", "gpt-4o-mini"],
    ),
    Provider(
        id="ollama",
        name="Local (Ollama)",
        description="자체 호스팅 LLM. 오프라인 워크로드용.",
        envKey="OLLAMA_HOST",
        status="미설정",
        models=["llama3.1:8b", "qwen2.5:14b"],
    ),
]
