export interface TopTab {
  to: string;
  label: string;
  end?: boolean;
}

export const TOP_TABS: TopTab[] = [
  { to: '/', label: '홈', end: true },
  { to: '/getting-started', label: '시작하기' },
  { to: '/agents', label: 'AI 에이전트' },
  { to: '/api-providers', label: 'API & 프로바이더' },
  { to: '/advanced', label: '고급기능' },
  { to: '/workloads', label: '워크로드' },
];
