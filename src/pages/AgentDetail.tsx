import { useParams } from 'react-router-dom';
import { AGENT_CATEGORIES, getAgentById } from '../data/agents';

export default function AgentDetail() {
  const { agentId } = useParams<{ agentId: string }>();
  const agent = agentId ? getAgentById(agentId) : undefined;

  if (!agent) {
    return (
      <section className="page__section">
        <div className="card">
          <h3 style={{ marginTop: 0 }}>에이전트를 찾을 수 없음</h3>
          <p className="muted">알 수 없는 ID: {agentId}</p>
        </div>
      </section>
    );
  }

  const category = AGENT_CATEGORIES.find((c) => c.id === agent.category);

  return (
    <section className="page__section">
      <div className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <span style={{ fontSize: 28, color: 'var(--accent-hover)' }}>{category?.icon}</span>
          <div style={{ flex: 1 }}>
            <h3 style={{ margin: 0 }}>{agent.name}</h3>
            <p className="muted" style={{ margin: '4px 0 0' }}>
              {agent.tagline}
            </p>
          </div>
          <span className="pill">{category?.label}</span>
        </div>

        <p style={{ marginTop: 16 }}>{agent.description}</p>

        <div className="grid grid--2" style={{ marginTop: 18 }}>
          <div>
            <div className="kv">
              <span className="kv__k">기본 모델</span>
              <code className="kv__v">{agent.defaultModel}</code>
            </div>
          </div>
          <div>
            <div className="kv">
              <span className="kv__k">태그</span>
              <div className="kv__v" style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                {agent.tags.map((t) => (
                  <span key={t} className="pill">
                    {t}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div style={{ marginTop: 18 }}>
          <div className="kv__k" style={{ marginBottom: 8 }}>
            핵심 기능
          </div>
          <ul className="list-reset" style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {agent.capabilities.map((cap) => (
              <li
                key={cap}
                style={{
                  padding: '8px 12px',
                  background: 'var(--bg-elev-2)',
                  border: '1px solid var(--border)',
                  borderRadius: 8,
                  fontSize: 13,
                }}
              >
                · {cap}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
