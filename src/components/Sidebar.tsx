import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { useAgentCategories, useAgents } from '../api/hooks';
import type { AgentCategoryId } from '../types/agent';
import './Sidebar.css';

/**
 * Left sidebar listing agent categories.
 *
 * Categories and agents are fetched from the backend via
 * useAgentCategories / useAgents. Both hooks fall back to the static
 * seed catalog as placeholderData so the sidebar stays usable when
 * the backend is offline (and tests render without a network).
 */
export default function Sidebar() {
  const { data: categories = [] } = useAgentCategories();
  const { data: agents = [] } = useAgents();

  const [expanded, setExpanded] = useState<Record<string, boolean>>({
    coding: true,
    analysis: true,
  });

  const toggle = (id: AgentCategoryId) => {
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <aside className="sidebar" aria-label="agent categories">
      <div className="sidebar__heading">에이전트</div>
      <ul className="sidebar__categories">
        {categories.map((category) => {
          const items = agents.filter((a) => a.category === category.id);
          const isOpen = expanded[category.id] ?? false;
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
                <span className="sidebar__category-count">{items.length}</span>
                <span
                  className={`sidebar__chevron${isOpen ? ' sidebar__chevron--open' : ''}`}
                  aria-hidden="true"
                >
                  ▾
                </span>
              </button>
              {isOpen && (
                <ul className="sidebar__agents">
                  {items.map((agent) => (
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
