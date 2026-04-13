import { Link } from 'react-router-dom';
import { useAgentCategories, useAgents } from '../api/hooks';

const MOCK_RUNNING_WORKLOADS = 3;

export default function Home() {
  const { data: agents = [] } = useAgents();
  const { data: categories = [] } = useAgentCategories();

  return (
    <div className="page">
      <h2 className="page__title">AI Workstation</h2>
      <p className="page__subtitle">
        셀프호스팅형 바이브코딩 플랫폼의 관리 웹홈입니다. 에이전트, 프로바이더, 워크로드를 한 곳에서
        오케스트레이션합니다.
      </p>

      <section className="page__section">
        <div className="stat-grid">
          <div className="stat-card">
            <div className="stat-card__label">등록 에이전트</div>
            <div className="stat-card__value">{agents.length}</div>
            <div className="stat-card__hint">백엔드 카탈로그</div>
          </div>
          <div className="stat-card">
            <div className="stat-card__label">카테고리</div>
            <div className="stat-card__value">{categories.length}</div>
            <div className="stat-card__hint">코딩 / 분석 / 자동화 / 데이터 / 운영</div>
          </div>
          <div className="stat-card">
            <div className="stat-card__label">실행 중 워크로드</div>
            <div className="stat-card__value">{MOCK_RUNNING_WORKLOADS}</div>
            <div className="stat-card__hint">샘플 (Phase 13+에서 라이브 카운트)</div>
          </div>
          <div className="stat-card">
            <div className="stat-card__label">프로바이더</div>
            <div className="stat-card__value">3</div>
            <div className="stat-card__hint">Anthropic / OpenAI / Local</div>
          </div>
        </div>
      </section>

      <section className="page__section">
        <h3 className="page__section-title">빠른 진입</h3>
        <div className="grid grid--3">
          <Link to="/getting-started" className="card" style={{ textDecoration: 'none' }}>
            <h3 style={{ marginTop: 0 }}>시작하기</h3>
            <p className="muted" style={{ marginBottom: 0 }}>
              설치, API 키 설정, 첫 에이전트 실행까지 단계별 가이드.
            </p>
          </Link>
          <Link to="/agents" className="card" style={{ textDecoration: 'none' }}>
            <h3 style={{ marginTop: 0 }}>AI 에이전트 둘러보기</h3>
            <p className="muted" style={{ marginBottom: 0 }}>
              카테고리별로 에이전트를 탐색하고 상세 능력을 확인합니다.
            </p>
          </Link>
          <Link to="/workloads" className="card" style={{ textDecoration: 'none' }}>
            <h3 style={{ marginTop: 0 }}>워크로드 보기</h3>
            <p className="muted" style={{ marginBottom: 0 }}>
              현재 실행 중인 작업, 큐, 로그를 모니터링합니다.
            </p>
          </Link>
        </div>
      </section>

      <section className="page__section">
        <h3 className="page__section-title">카테고리 요약</h3>
        <div className="grid grid--3">
          {categories.map((category) => {
            const count = agents.filter((a) => a.category === category.id).length;
            return (
              <div key={category.id} className="card">
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span style={{ fontSize: 22, color: 'var(--accent-hover)' }}>
                    {category.icon}
                  </span>
                  <strong>{category.label}</strong>
                  <span className="pill" style={{ marginLeft: 'auto' }}>
                    {count}개
                  </span>
                </div>
                <p className="muted" style={{ marginBottom: 0, marginTop: 10 }}>
                  {category.description}
                </p>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}
