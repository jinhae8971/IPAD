"""약세 분석 에이전트 - 부정적/신중한 시각에서 시장을 분석"""

from src.agents.base_llm_agent import BaseLLMAgent
from src.models import AgentAnalysis

SYSTEM_PROMPT = """당신은 신중하고 비판적인 시각을 가진 시니어 증시 분석가 '약세론자'입니다.
당신의 역할은:

1. 뉴스와 시장 상황에서 위험 신호와 하방 리스크를 찾아냅니다
2. 과열 징후와 버블 가능성을 분석합니다
3. 주의해야 할 섹터와 리스크 요인을 제시합니다
4. 헤지 전략과 방어적 포지션을 제안합니다

단, 근거 없는 비관은 삼가고, 구체적 데이터와 논리에 기반하여 분석하세요.
반드시 한국어로 답변하세요. 마크다운 형식을 사용하세요.
"""


class BearAnalyst(BaseLLMAgent):
    """약세 관점 분석 에이전트"""

    def __init__(self):
        super().__init__("약세 분석가", SYSTEM_PROMPT)

    def analyze(self, news_summary: str) -> AgentAnalysis:
        prompt = f"""다음은 오늘의 한미 증시 뉴스 분석 요약입니다:

{news_summary}

약세론자의 관점에서 다음을 분석해주세요:

## 🔴 위험 시그널
(시장에서 포착되는 경고 신호들)

## 📉 하방 리스크 분석
(단기/중기/장기 하락 요인)

## ⚠️ 주의 섹터 & 리스크
(경계해야 할 섹터와 그 이유)

## 🛡️ 방어 전략
(현재 시점에서의 헤지/방어 전략)

## ⚖️ 긍정 요인 인정
(약세론자로서도 인정해야 할 긍정적 요인)
"""
        content = self._call_llm(prompt, temperature=0.6)
        key_points = self._extract_key_points(content)

        return AgentAnalysis(
            agent_name=self.name,
            role="약세 관점 분석",
            content=content,
            key_points=key_points,
        )

    def _extract_key_points(self, content: str) -> list[str]:
        points = []
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped and (stripped.startswith("- ") or stripped.startswith("* ")):
                points.append(stripped[2:])
        return points[:8]
