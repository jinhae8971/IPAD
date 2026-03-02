"""LLM 기반 에이전트 베이스 클래스"""

import logging

from openai import OpenAI

from src.config import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)


class BaseLLMAgent:
    """OpenAI API를 사용하는 에이전트의 기본 클래스"""

    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

    def _call_llm(self, user_prompt: str, temperature: float = 0.7) -> str:
        """LLM API 호출"""
        if not self.client:
            logger.error(f"[{self.name}] OpenAI API 키가 설정되지 않았습니다.")
            return f"[{self.name}] API 키 미설정으로 분석을 수행할 수 없습니다."

        try:
            logger.info(f"  [{self.name}] LLM 분석 요청 중...")
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=4000,
            )
            result = response.choices[0].message.content
            logger.info(f"  [{self.name}] 분석 완료 ({len(result)}자)")
            return result
        except Exception as e:
            logger.error(f"  [{self.name}] LLM 호출 실패: {e}")
            return f"[{self.name}] 분석 중 오류 발생: {e}"
