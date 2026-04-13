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

- **프론트엔드**: Vite 5 + React 18 + TypeScript (strict)
- **라우팅**: react-router-dom v6 (HashRouter → GH Pages 친화)
- **테스트**: Vitest + jsdom + Testing Library
- **품질**: ESLint + Prettier + TypeScript typecheck
- **CI/CD**: GitHub Actions (CI + GH Pages 배포)

## 저장소 레이아웃

```
/
├── src/                            # AI Workstation 프론트엔드 (Vite+React+TS)
│   ├── components/                 # Layout, TopTabs, Sidebar, AgentCard
│   ├── pages/                      # Home, GettingStarted, Agents, AgentDetail,
│   │                               # ApiProviders, Advanced, Workloads
│   ├── data/agents.ts              # 에이전트 카탈로그 시드
│   ├── types/agent.ts              # 도메인 타입
│   ├── styles/                     # global.css, pages.css
│   └── router.tsx                  # HashRouter 구성
├── analyzer/                       # 기존 한미 증시 멀티에이전트 분석 시스템 (Python)
│   ├── src/ templates/ docs/ data/
│   └── requirements.txt
└── .github/workflows/
    ├── ci.yml                      # 포맷·린트·타입체크·테스트·빌드
    ├── deploy.yml                  # main 푸시 시 GH Pages 배포
    └── daily-analysis.yml          # 기존 Python 분석기 일일 실행
```

## 로컬 개발

```bash
npm install
npm run dev       # http://localhost:5173
```

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

모든 push · PR · 수동 실행에서 Node 22 환경으로 다음을 순차 실행합니다.

1. `npm ci`
2. `npm run format:check`
3. `npm run lint`
4. `npm run typecheck`
5. `npm test`
6. `npm run build`
7. `dist/` 업로드 (아티팩트 `workstation-dist`, 7일 보존)

### Deploy (`.github/workflows/deploy.yml`)

`main`(또는 `master`) 브랜치 push 시 `dist/`를 GitHub Pages로 배포합니다. `analyzer/docs/`가 존재하면 `dist/analyzer/`로 병합하여, 기존 증시 분석 리포트도 같은 사이트의 `/analyzer` 경로에서 볼 수 있게 합니다.

### Daily Analysis (`.github/workflows/daily-analysis.yml`)

매일 09:00 KST (UTC 00:00) `analyzer/` 디렉터리에서 Python 파이프라인을 실행하고 결과를 `analyzer/docs/`와 `analyzer/data/`에 커밋합니다.

## 에이전트 카탈로그 (시드)

- **코딩**: Code Architect / Code Implementer / Code Reviewer
- **분석**: Market Analyst (IPAD) / Doc Summarizer
- **자동화**: Workflow Runner / Scheduler
- **데이터**: Data Collector / Indexer
- **운영**: Deployer / Observer

카탈로그는 `src/data/agents.ts`에서 관리합니다. 실제 백엔드 연동은 후속 단계에서 추가됩니다.

## 환경 변수

| 이름 | 용도 |
|------|------|
| `ANTHROPIC_API_KEY` | Claude 호출 (기본 프로바이더) |
| `OPENAI_API_KEY` | OpenAI 호출 (선택) |
| `OLLAMA_HOST` | 로컬 LLM 엔드포인트 (선택) |

## 라이선스

MIT
