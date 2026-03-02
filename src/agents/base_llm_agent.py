"""LLM 기반 에이전트 베이스 클래스 (Anthropic Claude)"""

import logging
import os

import anthropic

logger = logging.getLogger(__name__)


def _get_api_key():
    return os.environ.get("ANTHROPIC_API_KEY", "")


def _get_model():
    return os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")


class BaseLLMAgent:
    """Anthropic Claude API를 사용하는 에이전트의 기본 클래스"""

    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        api_key = _get_api_key()
        self.client = anthropic.Anthropic(api_key=api_key) if api_key else None

    def _call_llm(self, user_prompt: str, temperature: float = 0.7) -> str:
        """Claude API 호출"""
        if not self.client:
            logger.error(f"[{self.name}] Anthropic API 키가 설정되지 않았습니다.")
            return f"[{self.name}] API 키 미설정으로 분석을 수행할 수 없습니다."

        try:
            logger.info(f"  [{self.name}] Claude 분석 요청 중...")
            response = self.client.messages.create(
                model=_get_model(),
                max_tokens=4000,
                temperature=temperature,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt},
                ],
            )
            result = response.content[0].text
            logger.info(f"  [{self.name}] 분석 완료 ({len(result)}자)")
            return result
        except Exception as e:
            logger.error(f"  [{self.name}] Claude 호출 실패: {e}")
            return f"[{self.name}] 분석 중 오류 발생: {e}"
