"""뉴스 수집 에이전트 - RSS 피드에서 한미 증시 뉴스를 수집"""

import logging
from datetime import datetime, timezone, timedelta

import feedparser

from src.config import KR_RSS_FEEDS, US_RSS_FEEDS, MAX_NEWS_AGE_HOURS, MAX_NEWS_PER_SOURCE
from src.models import NewsItem

logger = logging.getLogger(__name__)


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
