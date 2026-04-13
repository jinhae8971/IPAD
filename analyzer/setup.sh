#!/bin/bash
# 한미 증시 멀티에이전트 분석 시스템 - 초기 설정 스크립트
# 사용법: bash setup.sh

set -e

echo "================================================"
echo "  한미 증시 멀티에이전트 AI 분석 시스템 설정"
echo "================================================"
echo ""

# 1. gh CLI 확인
if ! command -v gh &> /dev/null; then
    echo "[ERROR] GitHub CLI(gh)가 설치되어 있지 않습니다."
    echo "  설치: https://cli.github.com/"
    exit 1
fi

# 2. 로그인 확인
if ! gh auth status &> /dev/null; then
    echo "[ERROR] GitHub에 로그인되어 있지 않습니다."
    echo "  실행: gh auth login"
    exit 1
fi

REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
echo "[OK] 레포지토리: $REPO"
echo ""

# 3. ANTHROPIC_API_KEY 설정
echo "--- Anthropic API 키 설정 ---"
if gh secret list | grep -q ANTHROPIC_API_KEY; then
    echo "[OK] ANTHROPIC_API_KEY가 이미 설정되어 있습니다."
    read -p "  다시 설정하시겠습니까? (y/N): " RESET_KEY
    if [ "$RESET_KEY" != "y" ] && [ "$RESET_KEY" != "Y" ]; then
        echo "  건너뜁니다."
    else
        read -sp "  Anthropic API Key를 입력하세요: " API_KEY
        echo ""
        echo "$API_KEY" | gh secret set ANTHROPIC_API_KEY
        echo "[OK] ANTHROPIC_API_KEY가 업데이트되었습니다."
    fi
else
    read -sp "  Anthropic API Key를 입력하세요: " API_KEY
    echo ""
    if [ -z "$API_KEY" ]; then
        echo "[WARN] API 키가 비어있습니다. 나중에 설정해주세요:"
        echo "  gh secret set ANTHROPIC_API_KEY"
    else
        echo "$API_KEY" | gh secret set ANTHROPIC_API_KEY
        echo "[OK] ANTHROPIC_API_KEY가 설정되었습니다."
    fi
fi
echo ""

# 4. GitHub Pages 설정
echo "--- GitHub Pages 설정 ---"
PAGES_STATUS=$(gh api "repos/$REPO/pages" 2>&1 || echo "NOT_FOUND")
if echo "$PAGES_STATUS" | grep -q "NOT_FOUND\|Not Found"; then
    echo "  GitHub Pages를 활성화합니다..."
    gh api "repos/$REPO/pages" \
        -X POST \
        -f "build_type=workflow" 2>/dev/null && echo "[OK] GitHub Pages가 활성화되었습니다." || {
        echo "[INFO] GitHub Pages를 수동으로 설정해주세요:"
        echo "  Settings > Pages > Source > GitHub Actions"
    }
else
    # 이미 있으면 source를 workflow로 변경 시도
    gh api "repos/$REPO/pages" \
        -X PUT \
        -f "build_type=workflow" 2>/dev/null && echo "[OK] GitHub Pages가 GitHub Actions로 설정되었습니다." || {
        echo "[OK] GitHub Pages가 이미 활성화되어 있습니다."
    }
fi
echo ""

# 5. 워크플로우 수동 실행
echo "--- 첫 분석 실행 ---"
read -p "  지금 첫 분석을 실행하시겠습니까? (Y/n): " RUN_NOW
if [ "$RUN_NOW" != "n" ] && [ "$RUN_NOW" != "N" ]; then
    DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')
    gh workflow run daily-analysis.yml --ref "$DEFAULT_BRANCH" 2>/dev/null && {
        echo "[OK] 워크플로우가 실행되었습니다!"
        echo "  확인: gh run list --workflow=daily-analysis.yml"
    } || {
        echo "[INFO] 워크플로우 수동 실행 실패. main 브랜치에 푸시하면 자동 실행됩니다."
    }
fi

echo ""
echo "================================================"
echo "  설정 완료!"
echo "  - 매일 오전 9시(KST) 자동 실행됩니다"
echo "  - 수동 실행: gh workflow run daily-analysis.yml"
echo "  - GitHub Pages URL은 Settings > Pages에서 확인"
echo "================================================"
