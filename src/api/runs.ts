import { ApiError } from './client';

export interface DocSummarizerRequest {
  text: string;
}

export interface DocSummarizerResponse {
  summary: string;
  quotes: string[];
  model: string;
  inputTokens: number;
  outputTokens: number;
  workloadId: string;
  durationSec: number;
}

const API_BASE = (import.meta.env.VITE_API_BASE as string | undefined) ?? '/api';

export async function runDocSummarizer(body: DocSummarizerRequest): Promise<DocSummarizerResponse> {
  const response = await fetch(`${API_BASE}/agents/doc-summarizer/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    let detail = `${response.status}`;
    try {
      const payload = (await response.json()) as { detail?: string };
      if (payload.detail) detail = payload.detail;
    } catch {
      /* ignore */
    }
    throw new ApiError(detail, response.status);
  }
  return (await response.json()) as DocSummarizerResponse;
}
