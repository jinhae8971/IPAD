# IPAD - 한미 증시 멀티에이전트 AI 분석 시스템

AI 에이전트가 매일 한국과 미국 증시 뉴스를 수집하고, 멀티에이전트 토론을 통해 중장기 트레이딩 인사이트를 제공하는 자동화 시스템입니다.

## 시스템 구조

```
뉴스 수집 -> 뉴스 분석 -> [강세/약세/기술적] 분석가 토론 -> 종합 인사이트 -> HTML 리포트
```

### 에이전트 구성

| 에이전트 | 역할 |
|---------|------|
| News Collector | 한미 증시 RSS 피드에서 뉴스 수집 |
| News Analyst | 뉴스 분류 및 핵심 이슈 도출 |
| Bull Analyst | 강세 관점 분석 (기회, 상승 촉매) |
| Bear Analyst | 약세 관점 분석 (리스크, 하방 요인) |
| Technical Analyst | 중립적 매크로/기술적 분석 |
| Synthesis Agent | 토론 종합 및 최종 인사이트 도출 |

## 설정

### 필수: Repository Secrets

| Secret | 설명 |
|--------|------|
| `OPENAI_API_KEY` | OpenAI API 키 |

### GitHub Pages 설정

1. Repository Settings > Pages
2. Source: **GitHub Actions** 선택

## 실행

### 자동 실행
- 매일 오전 9시 KST (GitHub Actions cron)

### 수동 실행
- GitHub Actions > "Daily Stock Market Analysis" > Run workflow

### 로컬 실행
```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
python src/main.py
```

## 기술 스택

- Python 3.11, OpenAI API (GPT-4o-mini)
- RSS 피드 (feedparser), Jinja2 템플릿
- GitHub Actions + GitHub Pages
