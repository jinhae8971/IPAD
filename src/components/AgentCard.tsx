import type { Agent } from '../types/agent';
import { AGENT_CATEGORIES } from '../data/agents';
import './AgentCard.css';

interface Props {
  agent: Agent;
  onClick?: (id: string) => void;
  active?: boolean;
}

export default function AgentCard({ agent, onClick, active }: Props) {
  const category = AGENT_CATEGORIES.find((c) => c.id === agent.category);
  return (
    <button
      type="button"
      className={`agent-card${active ? ' agent-card--active' : ''}`}
      onClick={() => onClick?.(agent.id)}
    >
      <div className="agent-card__header">
        <span className="agent-card__icon" aria-hidden="true">
          {category?.icon}
        </span>
        <div>
          <div className="agent-card__name">{agent.name}</div>
          <div className="agent-card__category">{category?.label}</div>
        </div>
      </div>
      <p className="agent-card__tagline">{agent.tagline}</p>
      <div className="agent-card__tags">
        {agent.tags.map((t) => (
          <span key={t} className="agent-card__tag">
            {t}
          </span>
        ))}
      </div>
    </button>
  );
}
