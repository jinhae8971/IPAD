"""Seed workload samples.

Phase 6 returns static samples. Phase 7+ will stream real execution
state from the agent runtime.
"""

from __future__ import annotations

from ..models import Workload

WORKLOADS: list[Workload] = [
    Workload(
        id="wl-0142",
        agent="Market Analyst",
        status="running",
        startedAt="2026-04-13 09:00 KST",
        durationSec=42,
        summary="한미 증시 일일 리포트 생성 중",
    ),
    Workload(
        id="wl-0141",
        agent="Code Reviewer",
        status="queued",
        startedAt="2026-04-13 08:58 KST",
        durationSec=0,
        summary="PR #17 리뷰 대기",
    ),
    Workload(
        id="wl-0140",
        agent="Indexer",
        status="success",
        startedAt="2026-04-13 08:30 KST",
        durationSec=87,
        summary="뉴스 임베딩 인덱스 갱신 완료",
    ),
    Workload(
        id="wl-0139",
        agent="Deployer",
        status="failed",
        startedAt="2026-04-13 08:12 KST",
        durationSec=19,
        summary="staging 헬스체크 실패 → 자동 롤백",
    ),
]
