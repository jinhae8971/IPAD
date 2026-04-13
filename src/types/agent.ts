/**
 * Domain types for the AI Workstation agent catalog.
 *
 * The sidebar groups agents by AgentCategory; each agent has a stable
 * id used for routing (`/agents/:agentId`) and is referenced by both
 * the sidebar and the AI 에이전트 page.
 */

export type AgentCategoryId =
  | 'coding'
  | 'analysis'
  | 'automation'
  | 'data'
  | 'ops';

export interface AgentCategory {
  id: AgentCategoryId;
  label: string;
  description: string;
  icon: string;
}

export interface Agent {
  id: string;
  name: string;
  category: AgentCategoryId;
  tagline: string;
  description: string;
  capabilities: string[];
  defaultModel: string;
  tags: string[];
}
