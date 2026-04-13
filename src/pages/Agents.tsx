import { useMemo, useState } from 'react';
import { Outlet, useMatch, useNavigate } from 'react-router-dom';
import { useAgentCategories, useAgents } from '../api/hooks';
import type { AgentCategoryId } from '../types/agent';
import AgentCard from '../components/AgentCard';

type Filter = AgentCategoryId | 'all';

export default function Agents() {
  const navigate = useNavigate();
  const match = useMatch('/agents/:agentId');
  const activeId = match?.params.agentId;

  const { data: agents = [] } = useAgents();
  const { data: categories = [] } = useAgentCategories();

  const [filter, setFilter] = useState<Filter>('all');
  const [query, setQuery] = useState('');

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return agents.filter((a) => {
      if (filter !== 'all' && a.category !== filter) return false;
      if (!q) return true;
      return (
        a.name.toLowerCase().includes(q) ||
        a.tagline.toLowerCase().includes(q) ||
        a.tags.some((t) => t.toLowerCase().includes(q))
      );
    });
  }, [filter, query, agents]);

  return (
    <div className="page">
      <h2 className="page__title">AI 에이전트</h2>
      <p className="page__subtitle">
        좌측 사이드바 또는 아래 카드로 에이전트를 탐색합니다. 선택 시 상세 정보가 표시됩니다.
      </p>

      <div className="toolbar">
        <input
          className="toolbar__search"
          type="search"
          placeholder="이름, 태그, 설명으로 검색"
          aria-label="에이전트 검색"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          type="button"
          className={`chip${filter === 'all' ? ' chip--active' : ''}`}
          onClick={() => setFilter('all')}
        >
          전체
        </button>
        {categories.map((c) => (
          <button
            type="button"
            key={c.id}
            className={`chip${filter === c.id ? ' chip--active' : ''}`}
            onClick={() => setFilter(c.id)}
          >
            {c.label}
          </button>
        ))}
      </div>

      {filtered.length === 0 ? (
        <p className="muted">조건에 맞는 에이전트가 없습니다.</p>
      ) : (
        <div className="grid grid--3">
          {filtered.map((agent) => (
            <AgentCard
              key={agent.id}
              agent={agent}
              active={agent.id === activeId}
              onClick={(id) => navigate(`/agents/${id}`)}
            />
          ))}
        </div>
      )}

      <Outlet />
    </div>
  );
}
