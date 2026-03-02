"""뉴스 소스 및 시스템 설정"""

import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

MAX_NEWS_AGE_HOURS = 48
MAX_NEWS_PER_SOURCE = 15
MAX_REPORT_DAYS = 30

KR_RSS_FEEDS = [
    {
        "name": "한국경제 증권",
        "url": "https://www.hankyung.com/feed/stock",
        "category": "KR",
    },
    {
        "name": "연합뉴스 경제",
        "url": "https://www.yna.co.kr/rss/economy.xml",
        "category": "KR",
    },
    {
        "name": "매일경제",
        "url": "https://www.mk.co.kr/rss/30100041/",
        "category": "KR",
    },
]

US_RSS_FEEDS = [
    {
        "name": "Yahoo Finance",
        "url": "https://finance.yahoo.com/news/rssindex",
        "category": "US",
    },
    {
        "name": "MarketWatch",
        "url": "https://feeds.marketwatch.com/marketwatch/topstories/",
        "category": "US",
    },
    {
        "name": "CNBC Market",
        "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258",
        "category": "US",
    },
    {
        "name": "Reuters Business",
        "url": "https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best",
        "category": "US",
    },
]

ALL_FEEDS = KR_RSS_FEEDS + US_RSS_FEEDS

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
REPORTS_DIR = os.path.join(DOCS_DIR, "reports")
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
