"""데이터 모델 정의"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class NewsItem:
    title: str
    summary: str
    link: str
    source: str
    category: str  # "KR" or "US"
    published: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "summary": self.summary,
            "link": self.link,
            "source": self.source,
            "category": self.category,
            "published": self.published.isoformat() if self.published else "",
        }


@dataclass
class AgentAnalysis:
    agent_name: str
    role: str
    content: str
    key_points: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "agent_name": self.agent_name,
            "role": self.role,
            "content": self.content,
            "key_points": self.key_points,
        }


@dataclass
class DailyReport:
    date: str
    kr_news: list[NewsItem] = field(default_factory=list)
    us_news: list[NewsItem] = field(default_factory=list)
    news_summary: Optional[AgentAnalysis] = None
    bull_analysis: Optional[AgentAnalysis] = None
    bear_analysis: Optional[AgentAnalysis] = None
    technical_analysis: Optional[AgentAnalysis] = None
    synthesis: Optional[AgentAnalysis] = None
    generated_at: str = ""

    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "kr_news": [n.to_dict() for n in self.kr_news],
            "us_news": [n.to_dict() for n in self.us_news],
            "news_summary": self.news_summary.to_dict() if self.news_summary else None,
            "bull_analysis": self.bull_analysis.to_dict() if self.bull_analysis else None,
            "bear_analysis": self.bear_analysis.to_dict() if self.bear_analysis else None,
            "technical_analysis": self.technical_analysis.to_dict() if self.technical_analysis else None,
            "synthesis": self.synthesis.to_dict() if self.synthesis else None,
            "generated_at": self.generated_at,
        }
