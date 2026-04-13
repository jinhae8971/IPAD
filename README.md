# AI Workstation

[![CI](https://github.com/jinhae8971/IPAD/actions/workflows/ci.yml/badge.svg?branch=claude/ai-workstation-setup-hXamX)](https://github.com/jinhae8971/IPAD/actions/workflows/ci.yml)
[![Deploy](https://github.com/jinhae8971/IPAD/actions/workflows/deploy.yml/badge.svg?branch=main)](https://github.com/jinhae8971/IPAD/actions/workflows/deploy.yml)

셀프호스팅형 바이브코딩 플랫폼의 관리 웹홈입니다. 에이전트, API 프로바이더, 고급 기능(훅·스킬·MCP·서브에이전트), 워크로드를 한 곳에서 오케스트레이션합니다.

## 탭 구성

| 탭 | 설명 |
|----|------|
| 홈 | 워크스테이션 개요 / 통계 / 빠른 진입 |
| 시작하기 | 설치 · 환경 변수 · 첫 에이전트 실행 가이드 |
| AI 에이전트 | 카테고리 필터 + 검색 + 상세(기본 모델, 태그, 능력) |
| API & 프로바이더 | Anthropic / OpenAI / Local(Ollama) 설정 |
| 고급기능 | 훅 · 스킬 · MCP · 서브에이전트 |
| 워크로드 | 실행 중/대기/완료/실패 작업 모니터 |

좌측 사이드바는 에이전트를 **코딩 / 분석 / 자동화 / 데이터 / 운영** 5개 카테고리로 분류하며, 항목 클릭 시 `AI 에이전트` 상세 페이지와 양방향 연동됩니다.

## 기술 스택

- **프론트엔드**: Vite 5 + React 18 + TypeScript (strict) + TanStack Query 5
- **백엔드**: FastAPI + Pydantic v2 + SQLite (stdlib sqlite3) + Anthropic SDK (Python 3.11)
- **라우팅**: react-router-dom v6 (HashRouter → GH Pages 친화)
- **테스트**: Vitest + jsdom + Testing Library / pytest
- **품질**: ESLint + Prettier + TypeScript typecheck
- **CI/CD**: GitHub Actions (frontend + backend CI + GH Pages 배포 + GHCR 이미지 푸시)

## 저장소 레이아웃

```
/
├── src/                            # AI Workstation 프론트엔드 (Vite+React+TS)
│   ├── api/                        # fetch client + TanStack Query hooks
│   ├── components/                 # Layout, TopTabs, Sidebar, AgentCard
│   ├── pages/                      # Home, GettingStarted, Agents, AgentDetail,
│   │                               # ApiProviders, Advanced, Workloads
│   ├── data/agents.ts              # 에이전트 카탈로그 (정적 fallback)
│   ├── types/agent.ts              # 도메인 타입
│   ├── styles/                     # global.css, pages.css
│   └── router.tsx                  # HashRouter 구성
├── backend/                        # FastAPI API 서버
│   ├── app/
│   │   ├── main.py                 # FastAPI 앱
│   │   ├── models.py               # Pydantic 모델
│   │   ├── db.py                   # SQLite 커넥션 + 스키마
│   │   ├── llm/client.py           # Anthropic SDK 래퍼 (테스트용 FakeLLM 지원)
│   │   ├── agents/                 # 실행형 에이전트 (doc_summarizer …)
│   │   ├── store/workloads.py      # SQLite-backed 워크로드 스토어
│   │   ├── data/                   # agents / providers / workloads 시드
│   │   └── routers/                # /api/agents /api/providers /api/workloads
│   ├── tests/                      # pytest (conftest로 임시 DB)
│   ├── Dockerfile                  # Python 멀티스테이지 + 비루트 실행
│   └── requirements.txt
├── analyzer/                       # ⚠ 별개 프로젝트 — 한미 증시 분석 시스템(IPAD)
│   │                               #    AI Workstation 백엔드와 통합되지 않으며,
│   │                               #    daily-analysis.yml 워크플로우로만 동작합니다.
│   ├── src/ templates/ docs/ data/
│   └── requirements.txt
├── Dockerfile                      # Frontend: Vite build → nginx serve
├── nginx.conf                      # SPA fallback + /api 리버스 프록시
├── docker-compose.yml              # web + api 스택
└── .github/workflows/
    ├── ci.yml                      # 프론트 + 백엔드 CI
    ├── deploy.yml                  # GH Pages 배포 + GHCR 이미지 푸시
    └── daily-analysis.yml          # 기존 Python 분석기 일일 실행
```

## 로컬 개발

프론트엔드와 백엔드를 두 개의 터미널에서 함께 실행합니다.

```bash
# Terminal 1 — Backend (FastAPI)
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --reload --port 8000
# OpenAPI 문서: http://localhost:8000/docs

# Terminal 2 — Frontend (Vite)
npm install
npm run dev       # http://localhost:5173  (/api 는 자동으로 :8000 으로 프록시)
```

프론트엔드는 백엔드가 꺼져 있어도 에이전트 카탈로그·카테고리 정적 시드로 동작합니다 (TanStack Query `placeholderData`). 프로바이더·워크로드 탭은 백엔드 응답을 직접 소비합니다.

## 셀프호스팅 (Docker Compose)

```bash
# Anthropic 키를 세션 환경 변수로 주입
export ANTHROPIC_API_KEY="sk-ant-..."

# 프론트(nginx) + 백엔드(uvicorn) 동시 기동
docker compose up --build

# → http://localhost:8080  (nginx 가 /api/* 를 api 서비스로 리버스 프록시)
```

구성:

- **`web`**: Vite 빌드 결과를 `nginx:1.27-alpine`이 서빙. `/api/*` 는 `api:8000`으로 프록시하고, 그 외 경로는 `index.html`로 SPA fallback.
- **`api`**: `python:3.11-slim` 기반 멀티스테이지 이미지. uvicorn으로 FastAPI 를 포트 8000에 바인드. 비루트 사용자 `app`으로 실행.
- **영속화**: `./data` 디렉터리가 컨테이너의 `/data` 로 마운트되어 SQLite DB(`workstation.db`)를 보관합니다. `docker compose down` 후 재기동해도 워크로드 이력이 유지되며, 리셋하려면 `./data/workstation.db` 를 삭제하면 됩니다.
- `web`은 `api`의 헬스체크(`/api/health`)가 통과한 뒤에만 기동합니다 (`depends_on.condition: service_healthy`).
- `docker compose down` 으로 정리.

두 이미지는 `deploy` 워크플로우가 `main` 푸시 시 GHCR 에 자동 빌드·푸시합니다 (`ghcr.io/<owner>/<repo>-web`, `-api`, 태그: `latest` + 커밋 SHA 7글자).

## 품질 게이트

CI와 동일한 순서로 로컬에서 실행할 수 있습니다.

```bash
npm run format:check   # Prettier
npm run lint           # ESLint
npm run typecheck      # TypeScript
npm test               # Vitest
npm run build          # 프로덕션 빌드 → dist/
```

## CI/CD

### CI (`.github/workflows/ci.yml`)

모든 push · PR · 수동 실행에서 두 개의 병렬 job이 실행됩니다.

**frontend** (Node 22)
1. `npm ci`
2. `npm run format:check`
3. `npm run lint`
4. `npm run typecheck`
5. `npm test`
6. `npm run build`
7. `dist/` 업로드 (아티팩트 `workstation-dist`, 7일 보존)

**backend** (Python 3.11)
1. `pip install -r backend/requirements.txt`
2. `PYTHONPATH=. pytest -q` (from `backend/`)

### Deploy (`.github/workflows/deploy.yml`)

`main`(또는 `master`) 브랜치 push 시 세 개의 job 이 실행됩니다.

1. **pages-build** — `npm run build` → `analyzer/docs/` 병합 → Pages 아티팩트 업로드
2. **pages-deploy** — GitHub Pages 환경으로 배포
3. **images** — 백엔드/프론트엔드 Docker 이미지를 GHCR에 병렬 빌드·푸시
   - `ghcr.io/<owner>/<repo>-api:latest`, `:<sha7>`
   - `ghcr.io/<owner>/<repo>-web:latest`, `:<sha7>`
   - Buildx + GHA cache(`type=gha`) 로 재빌드 비용 최소화

### Daily Analysis (`.github/workflows/daily-analysis.yml`)

매일 09:00 KST (UTC 00:00) `analyzer/` 디렉터리에서 Python 파이프라인을 실행하고 결과를 `analyzer/docs/`와 `analyzer/data/`에 커밋합니다.

## 에이전트 카탈로그 (시드)

- **코딩**: Code Architect / Code Implementer / Code Reviewer ✅ 실행 가능
- **분석**: Doc Summarizer ✅ 실행 가능
- **자동화**: Workflow Runner / Scheduler
- **데이터**: Data Collector / Indexer
- **운영**: Deployer / Observer

카탈로그의 source of truth는 `backend/app/data/agents.py` 입니다 (`GET /api/agents`로 노출). `src/data/agents.ts`는 백엔드가 꺼져 있을 때를 위한 placeholderData fallback입니다 (Phase 11 참고).

## 환경 변수

| 이름 | 용도 |
|------|------|
| `ANTHROPIC_API_KEY` | Claude 호출 (기본 프로바이더) |
| `OPENAI_API_KEY` | OpenAI 호출 (선택) |
| `OLLAMA_HOST` | 로컬 LLM 엔드포인트 (선택) |

## 라이선스

MIT
