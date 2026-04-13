import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { AGENT_CATEGORIES, getAgentsByCategory } from '../data/agents';
import type { AgentCategoryId } from '../types/agent';
import './Sidebar.css';

/**
 * Left sidebar listing agent categories.
 *
 * Each category can be expanded to show its agents. Clicking an agent
 * routes to /agents/:agentId, which renders inside the AI 에이전트 page.
 */
export default function Sidebar() {
  const [expanded, setExpanded] = useState<Record<AgentCategoryId, boolean>>({
    coding: true,
    analysis: true,
    automation: false,
    data: false,
    ops: false,
  });

  const toggle = (id: AgentCategoryId) => {
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <aside className="sidebar" aria-label="agent categories">
      <div className="sidebar__heading">에이전트</div>
      <ul className="sidebar__categories">
        {AGENT_CATEGORIES.map((category) => {
          const agents = getAgentsByCategory(category.id);
          const isOpen = expanded[category.id];
          return (
            <li key={category.id} className="sidebar__category">
              <button
                type="button"
                className="sidebar__category-button"
                aria-expanded={isOpen}
                onClick={() => toggle(category.id)}
              >
                <span className="sidebar__category-icon" aria-hidden="true">
                  {category.icon}
                </span>
                <span className="sidebar__category-label">{category.label}</span>
                <span className="sidebar__category-count">{agents.length}</span>
                <span
                  className={`sidebar__chevron${isOpen ? ' sidebar__chevron--open' : ''}`}
                  aria-hidden="true"
                >
                  ▾
                </span>
              </button>
              {isOpen && (
                <ul className="sidebar__agents">
                  {agents.map((agent) => (
                    <li key={agent.id}>
                      <NavLink
                        to={`/agents/${agent.id}`}
                        className={({ isActive }) =>
                          isActive ? 'sidebar__agent sidebar__agent--active' : 'sidebar__agent'
                        }
                      >
                        {agent.name}
                      </NavLink>
                    </li>
                  ))}
                </ul>
              )}
            </li>
          );
        })}
      </ul>
    </aside>
  );
}
