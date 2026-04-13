import { render, screen, waitFor } from '@testing-library/react';
import { RouterProvider, createMemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { vi } from 'vitest';
import WorkloadDetail from './WorkloadDetail';
import * as client from '../api/client';
import type { Workload } from '../api/hooks';

function renderAt(path: string) {
  const router = createMemoryRouter(
    [{ path: '/workloads/:workloadId', element: <WorkloadDetail /> }],
    { initialEntries: [path] },
  );
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>,
  );
}

describe('WorkloadDetail', () => {
  it('renders status, summary and JSON result for a successful workload', async () => {
    const workload: Workload = {
      id: 'wl-0250',
      agent: 'Doc Summarizer',
      status: 'success',
      startedAt: '2026-04-13 09:30 KST',
      durationSec: 4,
      summary: '요약 완료: 한 줄 요약',
      result: {
        summary: '한 줄 요약',
        quotes: ['인용 1', '인용 2'],
        model: 'claude-haiku-4-5',
      },
    };
    const spy = vi.spyOn(client, 'apiGet').mockResolvedValue(workload);

    const { container } = renderAt('/workloads/wl-0250');

    expect(await screen.findByText('wl-0250')).toBeInTheDocument();
    expect(screen.getByText('success')).toBeInTheDocument();
    expect(screen.getByText('Doc Summarizer')).toBeInTheDocument();
    expect(screen.getByText(/요약 완료/)).toBeInTheDocument();
    // JSON pretty-print is rendered into a <pre>; check the raw
    // textContent so the multi-line + whitespace does not break
    // Testing Library's normalized matcher.
    const pre = container.querySelector('pre');
    expect(pre).not.toBeNull();
    expect(pre!.textContent).toContain('한 줄 요약');
    expect(pre!.textContent).toContain('claude-haiku-4-5');
    expect(pre!.textContent).toContain('인용 1');

    expect(spy).toHaveBeenCalledWith('/workloads/wl-0250');
    spy.mockRestore();
  });

  it('shows a friendly message when a seed row has no result', async () => {
    const workload: Workload = {
      id: 'wl-0142',
      agent: 'Market Analyst',
      status: 'running',
      startedAt: '2026-04-13 09:00 KST',
      durationSec: 42,
      summary: '한미 증시 일일 리포트 생성 중',
      result: null,
    };
    const spy = vi.spyOn(client, 'apiGet').mockResolvedValue(workload);

    renderAt('/workloads/wl-0142');

    await waitFor(() => expect(screen.getByText('wl-0142')).toBeInTheDocument());
    expect(screen.getByText(/아직 결과가 기록되지 않았습니다/)).toBeInTheDocument();
    spy.mockRestore();
  });
});
