export default function GettingStarted() {
  return (
    <div className="page">
      <h2 className="page__title">시작하기</h2>
      <p className="page__subtitle">
        AI Workstation을 로컬에서 실행하고 첫 에이전트를 호출하기까지 걸리는 단계입니다.
      </p>

      <section className="page__section">
        <h3 className="page__section-title">1. 저장소 클론</h3>
        <pre className="code-block">{`git clone https://github.com/jinhae8971/IPAD.git
cd IPAD`}</pre>
      </section>

      <section className="page__section">
        <h3 className="page__section-title">2. 의존성 설치</h3>
        <pre className="code-block">{`# 프론트엔드
npm install

# 기존 분석기 (옵션)
cd analyzer && pip install -r requirements.txt && cd ..`}</pre>
      </section>

      <section className="page__section">
        <h3 className="page__section-title">3. 환경 변수 설정</h3>
        <p className="muted">프로젝트 루트의 <code>.env</code> 파일 또는 셸 환경에 설정합니다.</p>
        <pre className="code-block">{`export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."    # 선택
export OLLAMA_HOST="http://localhost:11434"  # 선택`}</pre>
      </section>

      <section className="page__section">
        <h3 className="page__section-title">4. 개발 서버 실행</h3>
        <pre className="code-block">{`npm run dev
# → http://localhost:5173`}</pre>
      </section>

      <section className="page__section">
        <h3 className="page__section-title">5. 품질 게이트</h3>
        <pre className="code-block">{`npm run lint       # ESLint
npm run typecheck  # TypeScript
npm test           # Vitest
npm run build      # 프로덕션 빌드`}</pre>
        <p className="muted">GitHub Actions CI가 PR마다 동일한 게이트를 실행합니다.</p>
      </section>
    </div>
  );
}
