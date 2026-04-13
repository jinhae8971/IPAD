"""HTML 리포트 생성기 - Jinja2 템플릿을 사용하여 정적 HTML 생성"""

import json
import logging
import os
import glob

from jinja2 import Environment, FileSystemLoader

from src.config import MARKET_DIR, REPORTS_DIR, TEMPLATES_DIR, DATA_DIR, MAX_REPORT_DAYS
from src.models import DailyReport

logger = logging.getLogger(__name__)


class ReportGenerator:
    """일별 분석 리포트를 HTML로 생성하는 클래스"""

    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(TEMPLATES_DIR),
            autoescape=True,
        )
        os.makedirs(REPORTS_DIR, exist_ok=True)
        os.makedirs(MARKET_DIR, exist_ok=True)
        os.makedirs(DATA_DIR, exist_ok=True)

    def generate(self, report: DailyReport) -> str:
        """일별 리포트 HTML 생성 및 인덱스 업데이트"""
        # 리포트 데이터를 JSON으로 저장
        data_path = os.path.join(DATA_DIR, f"{report.date}.json")
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
        logger.info(f"  리포트 데이터 저장: {data_path}")

        # 개별 리포트 HTML 생성
        report_html = self._render_report(report)
        report_path = os.path.join(REPORTS_DIR, f"{report.date}.html")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_html)
        logger.info(f"  리포트 HTML 생성: {report_path}")

        # 인덱스 페이지 업데이트
        self._update_index()

        # 오래된 리포트 정리
        self._cleanup_old_reports()

        return report_path

    def _render_report(self, report: DailyReport) -> str:
        template = self.env.get_template("report.html")
        return template.render(report=report)

    def _update_index(self):
        """인덱스 페이지를 최신 리포트 목록으로 업데이트"""
        report_files = sorted(
            glob.glob(os.path.join(REPORTS_DIR, "*.html")),
            reverse=True,
        )

        reports_info = []
        for f in report_files:
            date_str = os.path.basename(f).replace(".html", "")
            # 대응하는 JSON 데이터가 있으면 요약 정보 로드
            summary = ""
            data_path = os.path.join(DATA_DIR, f"{date_str}.json")
            if os.path.exists(data_path):
                try:
                    with open(data_path, "r", encoding="utf-8") as df:
                        data = json.load(df)
                        synthesis = data.get("synthesis", {})
                        if synthesis:
                            content = synthesis.get("content", "")
                            # 한줄 요약 추출
                            for line in content.split("\n"):
                                if "한줄 요약" in line or "한 줄 요약" in line:
                                    idx = content.index(line)
                                    remaining = content[idx + len(line):].strip()
                                    for l in remaining.split("\n"):
                                        l = l.strip()
                                        if l and not l.startswith("#"):
                                            summary = l.strip("*- >")
                                            break
                                    break
                        kr_count = len(data.get("kr_news", []))
                        us_count = len(data.get("us_news", []))
                except (json.JSONDecodeError, KeyError):
                    kr_count = 0
                    us_count = 0
            else:
                kr_count = 0
                us_count = 0

            reports_info.append({
                "date": date_str,
                "filename": os.path.basename(f),
                "summary": summary,
                "kr_count": kr_count,
                "us_count": us_count,
            })

        template = self.env.get_template("index.html")
        index_html = template.render(reports=reports_info)
        index_path = os.path.join(MARKET_DIR, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_html)
        logger.info(f"  인덱스 페이지 업데이트: {index_path}")

    def _cleanup_old_reports(self):
        """MAX_REPORT_DAYS일 이상 된 리포트 삭제"""
        report_files = sorted(glob.glob(os.path.join(REPORTS_DIR, "*.html")))
        if len(report_files) > MAX_REPORT_DAYS:
            to_remove = report_files[: len(report_files) - MAX_REPORT_DAYS]
            for f in to_remove:
                os.remove(f)
                date_str = os.path.basename(f).replace(".html", "")
                data_file = os.path.join(DATA_DIR, f"{date_str}.json")
                if os.path.exists(data_file):
                    os.remove(data_file)
                logger.info(f"  오래된 리포트 삭제: {f}")
