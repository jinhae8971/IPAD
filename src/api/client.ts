/**
 * Thin fetch wrapper for the AI Workstation backend.
 *
 * The base URL defaults to a same-origin `/api` path so it works both:
 *   1. Behind the Vite dev proxy (vite.config.ts → http://localhost:8000)
 *   2. When the frontend and backend are served from the same host.
 */

const API_BASE = (import.meta.env.VITE_API_BASE as string | undefined) ?? '/api';

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export async function apiGet<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    ...init,
    headers: { Accept: 'application/json', ...(init?.headers ?? {}) },
  });
  if (!response.ok) {
    throw new ApiError(`GET ${url} failed: ${response.status}`, response.status);
  }
  return (await response.json()) as T;
}
