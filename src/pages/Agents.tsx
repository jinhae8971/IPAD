import { Outlet, useMatch } from 'react-router-dom';

export default function Agents() {
  const match = useMatch('/agents/:agentId');
  return (
    <section>
      <h2>AI 에이전트</h2>
      {!match && (
        <p className="muted">
          좌측 사이드바에서 카테고리를 펼쳐 에이전트를 선택하면 상세가 여기에 표시됩니다. (Phase 3)
        </p>
      )}
      <Outlet />
    </section>
  );
}
