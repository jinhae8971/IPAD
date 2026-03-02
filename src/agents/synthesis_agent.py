"""종합 인사이트 에이전트 - 모든 분석가의 의견을 종합하여 최종 인사이트 도출"""

from src.agents.base_llm_agent import BaseLLMAgent
from src.models import AgentAnalysis

SYSTEM_PROMPT = """당신은 투자 전략 총괄 책임자(CIO)입니다.
세 명의 분석가(강세론자, 약세론자, 기술적 분석가)의 분석을 종합하여
최종 투자 인사이트와 전략을 수립합니다.

당신의 역할은:
1. 세 분석가의 의견이 일치하는 부분과 충돌하는 부분을 정리합니다
2. 근거의 강도를 평가하여 더 설득력 있는 논거를 판별합니다
3. 종합적인 시장 전망과 전략을 제시합니다
4. 구체적이고 실행 가능한 액션 아이템을 제공합니다
5. 리스크 관리 체크리스트를 작성합니다

편향되지 않은 균형 잡힌 시각으로 종합 판단하세요.
반드시 한국어로 답변하세요. 마크다운 형식을 사용하세요.
"""


class SynthesisAgent(BaseLLMAgent):
    """종합 인사이트 도출 에이전트"""

    def __init__(self):
        super().__init__("투자전략 총괄", SYSTEM_PROMPT)

    def synthesize(
        self,
        news_analysis: AgentAnalysis,
        bull_analysis: AgentAnalysis,
        bear_analysis: AgentAnalysis,
        technical_analysis: AgentAnalysis,
    ) -> AgentAnalysis:
        prompt = f"""다음은 오늘의 시장에 대한 세 분석가의 의견입니다.
이를 종합하여 최종 투자 인사이트를 도출해주세요.

---
### 📰 뉴스 분석 요약
{news_analysis.content}

---
### 🟢 강세 분석가 의견
{bull_analysis.content}

---
### 🔴 약세 분석가 의견
{bear_analysis.content}

---
### 📊 기술적 분석가 의견
{technical_analysis.content}

---

위 세 분석가의 의견을 종합하여 다음 형식으로 최종 인사이트를 작성해주세요:

## 🏛️ 토론 요약
(세 분석가의 핵심 주장 비교 및 합의/이견 사항)

## 🎯 종합 시장 전망
(현재 시장 상황에 대한 종합적 판단)

## 📋 중장기 투자 전략
(향후 1~6개월 관점의 전략적 방향)

## ✅ 액션 아이템
(구체적으로 실행할 수 있는 투자 행동 리스트)

## ⚠️ 리스크 체크리스트
(모니터링해야 할 리스크 요인과 대응 방안)

## 💬 한줄 요약
(오늘의 시장을 한 문장으로 정리)
"""
        content = self._call_llm(prompt, temperature=0.5)
        key_points = self._extract_key_points(content)

        return AgentAnalysis(
            agent_name=self.name,
            role="종합 인사이트 도출",
            content=content,
            key_points=key_points,
        )

    def _extract_key_points(self, content: str) -> list[str]:
        points = []
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped and (stripped.startswith("- ") or stripped.startswith("* ")):
                points.append(stripped[2:])
        return points[:10]
