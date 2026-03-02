"""기술적 분석 에이전트 - 중립적/데이터 기반으로 시장을 분석"""

from src.agents.base_llm_agent import BaseLLMAgent
from src.models import AgentAnalysis

SYSTEM_PROMPT = """당신은 중립적이고 데이터 중심적인 시니어 시장 분석가 '기술적 분석가'입니다.
당신의 역할은:

1. 감정을 배제하고 객관적 데이터와 매크로 지표를 기반으로 분석합니다
2. 금리, 환율, 유동성, 밸류에이션 등 거시 지표를 종합 판단합니다
3. 섹터 로테이션과 자금 흐름을 분석합니다
4. 중장기 트렌드와 사이클 관점에서 현재 위치를 진단합니다

강세/약세 편향 없이, 데이터가 말하는 바를 그대로 전달하세요.
반드시 한국어로 답변하세요. 마크다운 형식을 사용하세요.
"""


class TechnicalAnalyst(BaseLLMAgent):
    """중립적 기술/매크로 분석 에이전트"""

    def __init__(self):
        super().__init__("기술적 분석가", SYSTEM_PROMPT)

    def analyze(self, news_summary: str) -> AgentAnalysis:
        prompt = f"""다음은 오늘의 한미 증시 뉴스 분석 요약입니다:

{news_summary}

중립적 기술/매크로 분석가의 관점에서 다음을 분석해주세요:

## 📊 매크로 환경 진단
(금리, 환율, 유동성, 인플레이션 등 거시 지표 분석)

## 🔄 섹터 로테이션 분석
(자금 흐름과 섹터 간 이동 패턴)

## 📐 밸류에이션 점검
(현재 시장 밸류에이션 수준 판단)

## 📈 중장기 트렌드 진단
(현재 시장 사이클 위치와 트렌드 방향)

## 🎯 핵심 모니터링 지표
(향후 주목해야 할 주요 지표와 이벤트)
"""
        content = self._call_llm(prompt, temperature=0.4)
        key_points = self._extract_key_points(content)

        return AgentAnalysis(
            agent_name=self.name,
            role="중립적 기술/매크로 분석",
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
