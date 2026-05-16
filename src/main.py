"""메인 실행 스크립트 - 멀티에이전트 파이프라인 오케스트레이션"""

import logging
import sys
import os
from datetime import datetime, timezone, timedelta

# 프로젝트 루트를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Anthropic usage reporting (auto-reports each Claude call to central dashboard)
try:
    from src.anthropic_usage_reporter import patch_anthropic_client
    patch_anthropic_client(workflow="ipad-daily-analysis")
except Exception:
    pass

from src.agents.news_collector import NewsCollector
from src.agents.news_analyst import NewsAnalyst
from src.agents.bull_analyst import BullAnalyst
from src.agents.bear_analyst import BearAnalyst
from src.agents.technical_analyst import TechnicalAnalyst
from src.agents.synthesis_agent import SynthesisAgent
from src.report_generator import ReportGenerator
from src.models import DailyReport

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

KST = timezone(timedelta(hours=9))


def run_pipeline():
    """멀티에이전트 분석 파이프라인 실행"""
    today = datetime.now(KST).strftime("%Y-%m-%d")
    logger.info(f"{'='*60}")
    logger.info(f"  한미 증시 멀티에이전트 분석 시스템")
    logger.info(f"  날짜: {today}")
    logger.info(f"{'='*60}")

    report = DailyReport(date=today)

    # Phase 1: 뉴스 수집
    logger.info("\n[Phase 1] 뉴스 수집")
    collector = NewsCollector()
    kr_news, us_news = collector.collect_all()
    report.kr_news = kr_news
    report.us_news = us_news

    if not kr_news and not us_news:
        logger.warning("수집된 뉴스가 없습니다. 분석을 건너뜁니다.")
        report.generated_at = datetime.now(KST).isoformat()
        generator = ReportGenerator()
        generator.generate(report)
        return

    # Phase 2: 뉴스 분석
    logger.info("\n[Phase 2] 뉴스 분석 에이전트")
    analyst = NewsAnalyst()
    news_analysis = analyst.analyze(kr_news, us_news)
    report.news_summary = news_analysis
    logger.info("  뉴스 분석 완료")

    # Phase 3: 멀티에이전트 토론 (강세/약세/기술적 분석)
    logger.info("\n[Phase 3] 멀티에이전트 토론")
    news_context = news_analysis.content

    bull = BullAnalyst()
    bull_result = bull.analyze(news_context)
    report.bull_analysis = bull_result
    logger.info("  강세 분석 완료")

    bear = BearAnalyst()
    bear_result = bear.analyze(news_context)
    report.bear_analysis = bear_result
    logger.info("  약세 분석 완료")

    tech = TechnicalAnalyst()
    tech_result = tech.analyze(news_context)
    report.technical_analysis = tech_result
    logger.info("  기술적 분석 완료")

    # Phase 4: 종합 인사이트
    logger.info("\n[Phase 4] 종합 인사이트 도출")
    synthesizer = SynthesisAgent()
    synthesis = synthesizer.synthesize(news_analysis, bull_result, bear_result, tech_result)
    report.synthesis = synthesis
    logger.info("  종합 인사이트 완료")

    # Phase 5: 리포트 생성
    logger.info("\n[Phase 5] HTML 리포트 생성")
    report.generated_at = datetime.now(KST).isoformat()
    generator = ReportGenerator()
    report_path = generator.generate(report)
    logger.info(f"  리포트 생성 완료: {report_path}")

    logger.info(f"\n{'='*60}")
    logger.info("  분석 파이프라인 완료!")
    logger.info(f"{'='*60}")


if __name__ == "__main__":
    run_pipeline()
