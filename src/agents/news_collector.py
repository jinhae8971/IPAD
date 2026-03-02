"""뉴스 수집 에이전트 - RSS 피드에서 한미 증시 뉴스를 수집"""

import logging
import os
from datetime import datetime, timezone, timedelta

import feedparser

from src.config import KR_RSS_FEEDS, US_RSS_FEEDS, MAX_NEWS_AGE_HOURS, MAX_NEWS_PER_SOURCE
from src.models import NewsItem

logger = logging.getLogger(__name__)

# RSS 피드 접근 불가 시 사용할 샘플 뉴스 (테스트/데모용)
_SAMPLE_KR_NEWS = [
    {"title": "코스피, 외국인 순매수에 2,650선 회복...반도체주 강세", "summary": "외국인 투자자들이 반도체와 2차전지 관련주를 중심으로 순매수에 나서며 코스피가 2,650선을 회복했다. 삼성전자와 SK하이닉스가 상승을 주도했다.", "source": "한국경제 증권"},
    {"title": "한국은행 금리 동결, '경기 불확실성 고조' 언급", "summary": "한국은행이 기준금리를 3.00%로 동결하며 대내외 경기 불확실성이 커졌다고 밝혔다. 환율 변동성과 가계부채 관리에 주의가 필요하다고 강조했다.", "source": "연합뉴스 경제"},
    {"title": "2차전지 소재주 급등, LG에너지솔루션 실적 기대감", "summary": "LG에너지솔루션의 1분기 실적 개선 기대감에 2차전지 소재 관련주가 동반 상승했다. 에코프로비엠, 포스코퓨처엠 등이 강세를 보였다.", "source": "매일경제"},
    {"title": "삼성전자, HBM3E 양산 본격화...NVIDIA 납품 확대", "summary": "삼성전자가 HBM3E 양산을 본격화하며 NVIDIA향 납품을 확대한다. AI 반도체 수요 증가에 따른 수혜가 기대된다.", "source": "한국경제 증권"},
    {"title": "원달러 환율 1,350원대 안착, 수출기업 수혜 전망", "summary": "원달러 환율이 1,350원대에 안착하며 수출 기업들의 환율 수혜가 전망된다. 자동차, 조선 업종이 주목받고 있다.", "source": "연합뉴스 경제"},
    {"title": "코스닥, AI 관련주 중심 강세...900선 돌파 시도", "summary": "코스닥 시장이 AI 소프트웨어 및 반도체 관련주 중심으로 강세를 보이며 900선 돌파를 시도하고 있다.", "source": "매일경제"},
    {"title": "부동산 PF 리스크 완화 조짐, 건설주 반등", "summary": "정부의 부동산 PF 정상화 대책 발표 이후 건설주가 반등하고 있다. 대형 건설사 중심으로 투자심리가 개선되고 있다.", "source": "한국경제 증권"},
    {"title": "외국인, 한국 주식 3주 연속 순매수...IT·자동차 집중", "summary": "외국인 투자자가 3주 연속 한국 주식을 순매수하고 있다. 특히 IT와 자동차 업종에 집중 매수세가 이어지고 있다.", "source": "연합뉴스 경제"},
]

_SAMPLE_US_NEWS = [
    {"title": "S&P 500 hits new record as tech rally continues", "summary": "The S&P 500 reached a new all-time high driven by continued strength in technology stocks. NVIDIA and Microsoft led gains as AI investment optimism persists.", "source": "Yahoo Finance"},
    {"title": "Fed signals potential rate cuts in second half of 2026", "summary": "Federal Reserve officials signaled that rate cuts could come in the latter half of 2026 if inflation continues its downward trajectory. Markets reacted positively to the dovish tone.", "source": "MarketWatch"},
    {"title": "NVIDIA earnings beat expectations, AI demand surges", "summary": "NVIDIA reported quarterly earnings that exceeded analyst expectations, with data center revenue growing 80% year-over-year. The company raised its guidance citing unprecedented AI infrastructure demand.", "source": "CNBC Market"},
    {"title": "US-China trade tensions ease as new negotiations begin", "summary": "US and Chinese trade officials resumed negotiations, signaling a potential de-escalation of trade tensions. Markets rallied on hopes of reduced tariff barriers.", "source": "Reuters Business"},
    {"title": "Treasury yields drop as inflation data cools", "summary": "US Treasury yields fell after the latest CPI data showed inflation cooling to 2.4%, closer to the Fed's 2% target. Bond markets are pricing in earlier rate cuts.", "source": "MarketWatch"},
    {"title": "Apple announces $100B share buyback, stock surges", "summary": "Apple announced a massive $100 billion share buyback program alongside strong quarterly results. The stock surged 5% in after-hours trading.", "source": "Yahoo Finance"},
    {"title": "Oil prices fall on increased OPEC+ production plans", "summary": "Crude oil prices dropped 3% after OPEC+ signaled plans to increase production quotas. Energy stocks came under pressure as WTI crude fell below $70 per barrel.", "source": "CNBC Market"},
    {"title": "Regional banks rally on commercial real estate recovery signs", "summary": "Regional bank stocks rallied as data showed signs of recovery in the commercial real estate market. Analysts upgraded several mid-cap banks citing improving loan portfolios.", "source": "Reuters Business"},
]


class NewsCollector:
    """한국/미국 증시 뉴스를 RSS 피드에서 수집하는 에이전트"""

    def __init__(self):
        self.kr_feeds = KR_RSS_FEEDS
        self.us_feeds = US_RSS_FEEDS

    def collect_all(self) -> tuple[list[NewsItem], list[NewsItem]]:
        """모든 피드에서 뉴스를 수집하여 (한국, 미국) 뉴스 리스트 반환"""
        logger.info("=== 뉴스 수집 에이전트 시작 ===")

        kr_news = []
        for feed_info in self.kr_feeds:
            items = self._fetch_feed(feed_info)
            kr_news.extend(items)
            logger.info(f"  [{feed_info['name']}] {len(items)}건 수집")

        us_news = []
        for feed_info in self.us_feeds:
            items = self._fetch_feed(feed_info)
            us_news.extend(items)
            logger.info(f"  [{feed_info['name']}] {len(items)}건 수집")

        kr_news = self._deduplicate(kr_news)
        us_news = self._deduplicate(us_news)

        # RSS 피드에서 수집 실패 시 샘플 데이터로 폴백
        if not kr_news and not us_news:
            logger.info("  RSS 피드 수집 실패, 샘플 데이터 사용")
            kr_news, us_news = self._load_sample_news()

        logger.info(f"  총 수집: 한국 {len(kr_news)}건, 미국 {len(us_news)}건")
        return kr_news, us_news

    def _fetch_feed(self, feed_info: dict) -> list[NewsItem]:
        """단일 RSS 피드에서 뉴스 항목 수집"""
        items = []
        try:
            feed = feedparser.parse(feed_info["url"])
            cutoff = datetime.now(timezone.utc) - timedelta(hours=MAX_NEWS_AGE_HOURS)

            for entry in feed.entries[:MAX_NEWS_PER_SOURCE]:
                published = self._parse_date(entry)
                if published and published < cutoff:
                    continue

                title = entry.get("title", "").strip()
                summary = entry.get("summary", entry.get("description", "")).strip()
                # 요약이 너무 길면 잘라냄
                if len(summary) > 500:
                    summary = summary[:500] + "..."

                if not title:
                    continue

                items.append(
                    NewsItem(
                        title=title,
                        summary=summary,
                        link=entry.get("link", ""),
                        source=feed_info["name"],
                        category=feed_info["category"],
                        published=published,
                    )
                )
        except Exception as e:
            logger.warning(f"  피드 수집 실패 [{feed_info['name']}]: {e}")

        return items

    def _parse_date(self, entry) -> datetime | None:
        """RSS 엔트리에서 발행일 파싱"""
        date_fields = ["published_parsed", "updated_parsed", "created_parsed"]
        for field in date_fields:
            parsed = entry.get(field)
            if parsed:
                try:
                    from time import mktime
                    dt = datetime.fromtimestamp(mktime(parsed), tz=timezone.utc)
                    return dt
                except (ValueError, OverflowError, OSError):
                    continue
        return None

    def _load_sample_news(self) -> tuple[list[NewsItem], list[NewsItem]]:
        """RSS 수집 실패 시 샘플 뉴스 데이터 반환"""
        now = datetime.now(timezone.utc)
        kr = [
            NewsItem(
                title=n["title"], summary=n["summary"], link="",
                source=n["source"], category="KR", published=now,
            )
            for n in _SAMPLE_KR_NEWS
        ]
        us = [
            NewsItem(
                title=n["title"], summary=n["summary"], link="",
                source=n["source"], category="US", published=now,
            )
            for n in _SAMPLE_US_NEWS
        ]
        return kr, us

    def _deduplicate(self, items: list[NewsItem]) -> list[NewsItem]:
        """제목 기준으로 중복 뉴스 제거"""
        seen_titles = set()
        unique = []
        for item in items:
            normalized = item.title.lower().strip()
            if normalized not in seen_titles:
                seen_titles.add(normalized)
                unique.append(item)
        return unique
