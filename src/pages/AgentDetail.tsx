import { useParams } from 'react-router-dom';
import { getAgentById } from '../data/agents';

export default function AgentDetail() {
  const { agentId } = useParams<{ agentId: string }>();
  const agent = agentId ? getAgentById(agentId) : undefined;

  if (!agent) {
    return <p className="muted">알 수 없는 에이전트: {agentId}</p>;
  }

  return (
    <article style={{ marginTop: 16 }}>
      <h3 style={{ marginBottom: 4 }}>{agent.name}</h3>
      <p className="muted" style={{ marginTop: 0 }}>
        {agent.tagline}
      </p>
      <p>{agent.description}</p>
    </article>
  );
}
