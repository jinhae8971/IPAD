import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { vi } from 'vitest';
import DocSummarizerRunner from './DocSummarizerRunner';
import * as runs from '../api/runs';

function wrap(node: React.ReactNode) {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  return render(<QueryClientProvider client={client}>{node}</QueryClientProvider>);
}

describe('DocSummarizerRunner', () => {
  it('disables Run until text is entered', () => {
    wrap(<DocSummarizerRunner />);
    const button = screen.getByRole('button', { name: /Run Doc Summarizer/i });
    expect(button).toBeDisabled();

    fireEvent.change(screen.getByRole('textbox', { name: /요약할 문서/ }), {
      target: { value: 'hello world' },
    });
    expect(button).not.toBeDisabled();
  });

  it('renders summary, quotes, and metadata on success', async () => {
    const spy = vi.spyOn(runs, 'runDocSummarizer').mockResolvedValue({
      summary: '간단한 요약입니다.',
      quotes: ['중요 인용', '두번째 인용'],
      model: 'claude-haiku-4-5',
      inputTokens: 42,
      outputTokens: 18,
      workloadId: 'wl-0201',
      durationSec: 3,
    });

    wrap(<DocSummarizerRunner />);
    fireEvent.change(screen.getByRole('textbox', { name: /요약할 문서/ }), {
      target: { value: '요약할 원문' },
    });
    fireEvent.click(screen.getByRole('button', { name: /Run Doc Summarizer/i }));

    expect(await screen.findByText('간단한 요약입니다.')).toBeInTheDocument();
    expect(screen.getByText(/중요 인용/)).toBeInTheDocument();
    expect(screen.getByText(/두번째 인용/)).toBeInTheDocument();
    expect(screen.getByText('wl-0201')).toBeInTheDocument();
    expect(screen.getByText(/model: claude-haiku-4-5/)).toBeInTheDocument();

    expect(spy).toHaveBeenCalledWith({ text: '요약할 원문' });

    await waitFor(() => expect(spy).toHaveBeenCalledTimes(1));
    spy.mockRestore();
  });

  it('surfaces backend errors', async () => {
    const spy = vi.spyOn(runs, 'runDocSummarizer').mockRejectedValue(new Error('LLM call failed'));

    wrap(<DocSummarizerRunner />);
    fireEvent.change(screen.getByRole('textbox', { name: /요약할 문서/ }), {
      target: { value: 'bad input' },
    });
    fireEvent.click(screen.getByRole('button', { name: /Run Doc Summarizer/i }));

    expect(await screen.findByText(/에러: LLM call failed/)).toBeInTheDocument();
    spy.mockRestore();
  });
});
