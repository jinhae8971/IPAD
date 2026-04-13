import { render, screen, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { vi } from 'vitest';
import CodeReviewerRunner from './CodeReviewerRunner';
import * as runs from '../api/runs';

function wrap(node: React.ReactNode) {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  return render(<QueryClientProvider client={client}>{node}</QueryClientProvider>);
}

describe('CodeReviewerRunner', () => {
  it('disables Run until a diff is entered', () => {
    wrap(<CodeReviewerRunner />);
    const button = screen.getByRole('button', { name: /Run Code Reviewer/i });
    expect(button).toBeDisabled();

    fireEvent.change(screen.getByRole('textbox', { name: /리뷰할 diff/ }), {
      target: { value: '--- a\n+++ b' },
    });
    expect(button).not.toBeDisabled();
  });

  it('renders summary, comments (severity-pilled) and metadata on success', async () => {
    const spy = vi.spyOn(runs, 'runCodeReviewer').mockResolvedValue({
      summary: '대체로 안전한 변경입니다.',
      comments: [
        {
          file: 'src/foo.py',
          line: 12,
          severity: 'critical',
          message: 'count가 0일 때 ZeroDivisionError 발생',
        },
        {
          file: 'src/foo.py',
          line: 12,
          severity: 'warning',
          message: '0으로 나누기 위험이 남아있습니다',
        },
      ],
      model: 'claude-sonnet-4-6',
      inputTokens: 321,
      outputTokens: 64,
      workloadId: 'wl-0250',
      durationSec: 5,
    });

    wrap(<CodeReviewerRunner />);
    fireEvent.change(screen.getByRole('textbox', { name: /리뷰할 diff/ }), {
      target: { value: 'diff --git a/x b/x' },
    });
    fireEvent.change(screen.getByRole('textbox', { name: /리뷰 컨텍스트/ }), {
      target: { value: 'PR #42' },
    });
    fireEvent.click(screen.getByRole('button', { name: /Run Code Reviewer/i }));

    expect(await screen.findByText('대체로 안전한 변경입니다.')).toBeInTheDocument();
    expect(screen.getByText(/ZeroDivisionError/)).toBeInTheDocument();
    expect(screen.getByText(/0으로 나누기 위험/)).toBeInTheDocument();
    expect(screen.getByText('critical')).toBeInTheDocument();
    expect(screen.getByText('warning')).toBeInTheDocument();
    expect(screen.getByText('wl-0250')).toBeInTheDocument();
    expect(screen.getByText(/model: claude-sonnet-4-6/)).toBeInTheDocument();

    expect(spy).toHaveBeenCalledWith({ diff: 'diff --git a/x b/x', context: 'PR #42' });
    spy.mockRestore();
  });

  it('surfaces backend errors', async () => {
    const spy = vi.spyOn(runs, 'runCodeReviewer').mockRejectedValue(new Error('LLM call failed'));

    wrap(<CodeReviewerRunner />);
    fireEvent.change(screen.getByRole('textbox', { name: /리뷰할 diff/ }), {
      target: { value: 'broken diff' },
    });
    fireEvent.click(screen.getByRole('button', { name: /Run Code Reviewer/i }));

    expect(await screen.findByText(/에러: LLM call failed/)).toBeInTheDocument();
    spy.mockRestore();
  });
});
