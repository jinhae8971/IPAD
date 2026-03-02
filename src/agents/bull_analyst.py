"""강세 분석 에이전트 - 긍정적 시각에서 시장을 분석"""

from src.agents.base_llm_agent import BaseLLMAgent
from src.models import AgentAnalysis

SYSTEM_PROMPT = """당신은 낙관적 시각을 가진 시니어 증시 분석가 '강세론자'입니다.
당신의 역할은:

1. 뉴스와 시장 상황에서 긍정적 신호와 기회를 찾아냅니다
2. 상승 촉매와 성장 동력을 분석합니다
3. 유망한 섹터와 투자 기회를 제시합니다
4. 역발상 투자 관점에서 과매도 구간의 기회를 찾습니다

단, 근거 없는 낙관은 삼가고, 구체적 데이터와 논리에 기반하여 분석하세요.
반드시 한국어로 답변하세요. 마크다운 형식을 사용하세요.
"""


class BullAnalyst(BaseLLMAgent):
    """강세 관점 분석 에이전트"""

    def __init__(self):
        super().__init__("강세 분석가", SYSTEM_PROMPT)

    def analyze(self, news_summary: str) -> AgentAnalysis:
        prompt = f"""다음은 오늘의 한미 증시 뉴스 분석 요약입니다:

{news_summary}

강세론자의 관점에서 다음을 분석해주세요:

## 🟢 긍정적 시그널
(시장에서 포착되는 긍정적 신호들)

## 📈 상승 촉매 분석
(단기/중기/장기 상승 요인)

## 🌟 유망 섹터 & 테마
(주목해야 할 섹터와 그 이유)

## 💡 투자 기회
(현재 시점에서의 매수 기회 분석)

## ⚖️ 리스크 인정
(강세론자로서도 인정해야 할 리스크 요인)
"""
        content = self._call_llm(prompt, temperature=0.6)
        key_points = self._extract_key_points(content)

        return AgentAnalysis(
            agent_name=self.name,
            role="강세 관점 분석",
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
