import type { Agent, AgentCategory } from '../types/agent';

/**
 * Static seed for the AI Workstation agent catalog.
 *
 * Source of truth as of Phase 11 lives in the backend
 * (``backend/app/data/agents.py``) and is exposed via
 * ``GET /api/agents`` + ``GET /api/agents/categories``. This file is
 * imported by ``src/api/hooks.ts`` only to populate React Query's
 * ``placeholderData`` so the UI stays usable when the backend is
 * unreachable (e.g. during tests or static GH Pages preview).
 *
 * Keep this file in sync when adding new seed agents — both copies
 * exist for resilience, but the backend remains authoritative.
 */

export const AGENT_CATEGORIES: AgentCategory[] = [
  {
    id: 'coding',
    label: '코딩',
    description: '코드 작성, 리뷰, 리팩토링을 돕는 에이전트',
    icon: '⌨',
  },
  {
    id: 'analysis',
    label: '분석',
    description: '데이터·문서·시장 분석 에이전트',
    icon: '◎',
  },
  {
    id: 'automation',
    label: '자동화',
    description: '반복 작업을 워크플로우로 자동화',
    icon: '↻',
  },
  {
    id: 'data',
    label: '데이터',
    description: '수집·정제·인덱싱·검색 파이프라인',
    icon: '▤',
  },
  {
    id: 'ops',
    label: '운영',
    description: '배포·모니터링·인시던트 대응',
    icon: '⚙',
  },
];

export const AGENTS: Agent[] = [
  // Coding
  {
    id: 'code-architect',
    name: 'Code Architect',
    category: 'coding',
    tagline: '설계 단계부터 함께하는 시니어 엔지니어',
    description:
      '요구사항을 받아 모듈 경계, 데이터 모델, API 계약을 설계하고, 단계적 구현 계획을 제시합니다.',
    capabilities: [
      '요구사항 → 아키텍처 다이어그램 변환',
      '모듈/패키지 구조 제안',
      '단계별 구현 로드맵 생성',
    ],
    defaultModel: 'claude-opus-4-6',
    tags: ['architecture', 'planning', 'design'],
  },
  {
    id: 'code-implementer',
    name: 'Code Implementer',
    category: 'coding',
    tagline: '계획을 코드로 옮기는 실행형 에이전트',
    description:
      '주어진 사양과 코드베이스 컨벤션에 맞춰 파일을 생성·수정하고, 테스트를 함께 작성합니다.',
    capabilities: ['파일 단위 편집', '테스트 작성', '컨벤션 추적'],
    defaultModel: 'claude-sonnet-4-6',
    tags: ['implementation', 'testing'],
  },
  {
    id: 'code-reviewer',
    name: 'Code Reviewer',
    category: 'coding',
    tagline: '독립적인 시각의 PR 리뷰어',
    description:
      '변경 사항의 의도와 위험을 분리하여 평가하고, 잠재적 회귀와 보안 이슈를 표시합니다.',
    capabilities: ['diff 기반 리뷰', '회귀 위험 식별', '보안 점검'],
    defaultModel: 'claude-sonnet-4-6',
    tags: ['review', 'quality', 'security'],
  },

  // Analysis
  {
    id: 'market-analyst',
    name: 'Market Analyst',
    category: 'analysis',
    tagline: '한미 증시 멀티에이전트 분석 (IPAD)',
    description: '뉴스 수집·요약·강세/약세/기술 토론을 거쳐 중장기 트레이딩 인사이트를 도출합니다.',
    capabilities: ['RSS 수집', '멀티에이전트 토론', '리포트 생성'],
    defaultModel: 'claude-haiku-4-5',
    tags: ['finance', 'multi-agent', 'reporting'],
  },
  {
    id: 'doc-summarizer',
    name: 'Doc Summarizer',
    category: 'analysis',
    tagline: '긴 문서를 핵심만 남기는 요약가',
    description: '구조 보존 요약과 인용 추출, 토픽 클러스터링을 수행합니다.',
    capabilities: ['구조 보존 요약', '인용 추출', '토픽 클러스터링'],
    defaultModel: 'claude-haiku-4-5',
    tags: ['summarization', 'rag-prep'],
  },

  // Automation
  {
    id: 'workflow-runner',
    name: 'Workflow Runner',
    category: 'automation',
    tagline: '단계별 작업 흐름을 실행',
    description: '체크포인트와 재시도 정책을 가진 워크플로우 실행기.',
    capabilities: ['DAG 실행', '재시도/백오프', '체크포인트'],
    defaultModel: 'claude-haiku-4-5',
    tags: ['workflow', 'orchestration'],
  },
  {
    id: 'scheduler',
    name: 'Scheduler',
    category: 'automation',
    tagline: '크론·이벤트 기반 작업 스케줄러',
    description: '시간/이벤트 트리거로 다른 에이전트를 호출합니다.',
    capabilities: ['cron 표현식', '이벤트 훅', '실패 알림'],
    defaultModel: 'claude-haiku-4-5',
    tags: ['cron', 'triggers'],
  },

  // Data
  {
    id: 'data-collector',
    name: 'Data Collector',
    category: 'data',
    tagline: 'RSS·API·웹에서 데이터 수집',
    description: '소스별 어댑터로 원천 데이터를 수집·정제합니다.',
    capabilities: ['RSS/HTTP/RSS 어댑터', '중복 제거', '스키마 검증'],
    defaultModel: 'claude-haiku-4-5',
    tags: ['ingest', 'etl'],
  },
  {
    id: 'indexer',
    name: 'Indexer',
    category: 'data',
    tagline: '벡터·전문 검색 인덱스 구축',
    description: '청크 분할, 임베딩, 인덱스 갱신을 담당합니다.',
    capabilities: ['청킹', '임베딩', '인덱스 갱신'],
    defaultModel: 'claude-haiku-4-5',
    tags: ['embeddings', 'search'],
  },

  // Ops
  {
    id: 'deployer',
    name: 'Deployer',
    category: 'ops',
    tagline: '안전한 단계 배포 담당',
    description: '카나리/블루-그린 전략과 헬스체크 기반 롤백을 수행합니다.',
    capabilities: ['카나리/블루-그린', '헬스체크', '자동 롤백'],
    defaultModel: 'claude-sonnet-4-6',
    tags: ['deploy', 'rollback'],
  },
  {
    id: 'observer',
    name: 'Observer',
    category: 'ops',
    tagline: '메트릭·로그·트레이스 감시자',
    description: '이상 탐지와 인시던트 트리아지를 보조합니다.',
    capabilities: ['이상 탐지', '인시던트 트리아지', '온콜 알림'],
    defaultModel: 'claude-sonnet-4-6',
    tags: ['observability', 'incident'],
  },
];

export function getAgentsByCategory(categoryId: string): Agent[] {
  return AGENTS.filter((a) => a.category === categoryId);
}

export function getAgentById(id: string): Agent | undefined {
  return AGENTS.find((a) => a.id === id);
}
