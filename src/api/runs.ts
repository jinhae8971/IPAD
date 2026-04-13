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

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
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
  return (await response.json()) as T;
}

export async function runDocSummarizer(body: DocSummarizerRequest): Promise<DocSummarizerResponse> {
  return postJson<DocSummarizerResponse>('/agents/doc-summarizer/run', body);
}

export type ReviewSeverity = 'info' | 'warning' | 'critical';

export interface CodeReviewComment {
  file: string;
  line: number;
  severity: ReviewSeverity;
  message: string;
}

export interface CodeReviewerRequest {
  diff: string;
  context?: string;
}

export interface CodeReviewerResponse {
  summary: string;
  comments: CodeReviewComment[];
  model: string;
  inputTokens: number;
  outputTokens: number;
  workloadId: string;
  durationSec: number;
}

export async function runCodeReviewer(body: CodeReviewerRequest): Promise<CodeReviewerResponse> {
  return postJson<CodeReviewerResponse>('/agents/code-reviewer/run', body);
}
