import { useQuery } from '@tanstack/react-query';
import { apiGet } from './client';
import type { Agent, AgentCategory } from '../types/agent';
import { AGENTS, AGENT_CATEGORIES } from '../data/agents';

export interface Provider {
  id: string;
  name: string;
  description: string;
  envKey: string;
  status: '사용 가능' | '연결 대기' | '미설정';
  models: string[];
}

export interface Workload {
  id: string;
  agent: string;
  status: 'running' | 'queued' | 'success' | 'failed';
  startedAt: string;
  durationSec: number;
  summary: string;
  result?: Record<string, unknown> | null;
}

/**
 * All query hooks fall back to the static seed catalog when the API is
 * unreachable, so the web home stays usable without the backend running.
 */

export function useAgents() {
  return useQuery<Agent[]>({
    queryKey: ['agents'],
    queryFn: () => apiGet<Agent[]>('/agents'),
    placeholderData: AGENTS,
    retry: 1,
    staleTime: 60_000,
  });
}

export function useAgentCategories() {
  return useQuery<AgentCategory[]>({
    queryKey: ['agents', 'categories'],
    queryFn: () => apiGet<AgentCategory[]>('/agents/categories'),
    placeholderData: AGENT_CATEGORIES,
    retry: 1,
    staleTime: 5 * 60_000,
  });
}

export function useProviders() {
  return useQuery<Provider[]>({
    queryKey: ['providers'],
    queryFn: () => apiGet<Provider[]>('/providers'),
    retry: 1,
    staleTime: 60_000,
  });
}

export function useWorkloads() {
  return useQuery<Workload[]>({
    queryKey: ['workloads'],
    queryFn: () => apiGet<Workload[]>('/workloads'),
    retry: 1,
    refetchInterval: 15_000,
  });
}

export function useWorkload(id: string | undefined) {
  return useQuery<Workload>({
    queryKey: ['workloads', id],
    queryFn: () => apiGet<Workload>(`/workloads/${id}`),
    enabled: Boolean(id),
    retry: 1,
  });
}
