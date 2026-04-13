"""뉴스 분석 에이전트 - 수집된 뉴스를 분류하고 핵심 이슈를 도출"""

from src.agents.base_llm_agent import BaseLLMAgent
from src.models import NewsItem, AgentAnalysis

SYSTEM_PROMPT = """당신은 한국과 미국 증시 전문 뉴스 분석가입니다.
수집된 뉴스를 분석하여 다음을 수행합니다:

1. 뉴스를 카테고리별로 분류 (매크로경제, 섹터/산업, 개별종목, 정책/규제, 글로벌이벤트)
2. 가장 중요한 핵심 이슈 5~10개를 도출
3. 각 이슈의 시장 영향도를 상/중/하로 평가
4. 한국과 미국 시장 간의 연관성 분석

반드시 한국어로 답변하세요.
구조화된 형태로 정리하되, 마크다운 형식을 사용하세요.
"""


class NewsAnalyst(BaseLLMAgent):
    """뉴스 분류 및 핵심 이슈 도출 에이전트"""

    def __init__(self):
        super().__init__("뉴스 분석가", SYSTEM_PROMPT)

    def analyze(self, kr_news: list[NewsItem], us_news: list[NewsItem]) -> AgentAnalysis:
        news_text = self._format_news(kr_news, us_news)
        prompt = f"""다음은 오늘 수집된 한국과 미국 증시 관련 뉴스입니다.
이 뉴스들을 분석하여 핵심 이슈를 도출하고, 카테고리별로 분류해주세요.

{news_text}

다음 형식으로 분석해주세요:
## 📊 오늘의 핵심 이슈
(가장 중요한 이슈 5~10개, 영향도 표시)

## 🇰🇷 한국 시장 주요 뉴스
(카테고리별 정리)

## 🇺🇸 미국 시장 주요 뉴스
(카테고리별 정리)

## 🔗 한미 시장 연관성
(두 시장 간 상호 영향 분석)
"""
        content = self._call_llm(prompt, temperature=0.3)
        key_points = self._extract_key_points(content)

        return AgentAnalysis(
            agent_name=self.name,
            role="뉴스 분석 및 이슈 도출",
            content=content,
            key_points=key_points,
        )

    def _format_news(self, kr_news: list[NewsItem], us_news: list[NewsItem]) -> str:
        lines = ["### 한국 뉴스"]
        for i, news in enumerate(kr_news[:20], 1):
            lines.append(f"{i}. [{news.source}] {news.title}")
            if news.summary:
                lines.append(f"   요약: {news.summary[:200]}")

        lines.append("\n### 미국 뉴스")
        for i, news in enumerate(us_news[:20], 1):
            lines.append(f"{i}. [{news.source}] {news.title}")
            if news.summary:
                lines.append(f"   요약: {news.summary[:200]}")

        return "\n".join(lines)

    def _extract_key_points(self, content: str) -> list[str]:
        points = []
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped and (stripped.startswith("- ") or stripped.startswith("* ")):
                points.append(stripped[2:])
            elif stripped and len(stripped) > 2 and stripped[0].isdigit() and stripped[1] in ".)":
                points.append(stripped[2:].strip())
        return points[:10]
