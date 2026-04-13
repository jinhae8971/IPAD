import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { runDocSummarizer, type DocSummarizerResponse } from '../api/runs';

/**
 * Run panel embedded in the Doc Summarizer agent detail view.
 *
 * POSTs the textarea contents to /api/agents/doc-summarizer/run and
 * invalidates the workloads query so the new workload shows up in the
 * Workloads tab immediately.
 */
export default function DocSummarizerRunner() {
  const [text, setText] = useState('');
  const queryClient = useQueryClient();

  const mutation = useMutation<DocSummarizerResponse, Error, string>({
    mutationFn: (input) => runDocSummarizer({ text: input }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workloads'] });
    },
  });

  const canRun = text.trim().length > 0 && !mutation.isPending;

  return (
    <div style={{ marginTop: 20 }}>
      <div className="kv__k" style={{ marginBottom: 8 }}>
        실행
      </div>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="요약할 문서 텍스트를 붙여넣으세요"
        aria-label="요약할 문서"
        rows={6}
        style={{
          width: '100%',
          padding: '10px 12px',
          background: 'var(--bg-elev-2)',
          border: '1px solid var(--border)',
          borderRadius: 8,
          color: 'var(--text)',
          fontFamily: 'inherit',
          fontSize: 13,
          resize: 'vertical',
        }}
      />
      <div style={{ display: 'flex', gap: 10, marginTop: 10, alignItems: 'center' }}>
        <button
          type="button"
          disabled={!canRun}
          onClick={() => mutation.mutate(text)}
          style={{
            padding: '8px 16px',
            background: canRun ? 'var(--accent)' : 'var(--bg-elev-2)',
            color: canRun ? '#fff' : 'var(--text-muted)',
            border: '1px solid var(--border)',
            borderRadius: 8,
            cursor: canRun ? 'pointer' : 'not-allowed',
            fontSize: 13,
          }}
        >
          {mutation.isPending ? '실행 중...' : 'Run Doc Summarizer'}
        </button>
        {mutation.isError && (
          <span className="pill pill--danger">에러: {mutation.error.message}</span>
        )}
      </div>

      {mutation.data && (
        <div className="card" style={{ marginTop: 16 }}>
          <div className="kv__k" style={{ marginBottom: 6 }}>
            요약
          </div>
          <p style={{ margin: '0 0 14px' }}>{mutation.data.summary}</p>

          {mutation.data.quotes.length > 0 && (
            <>
              <div className="kv__k" style={{ marginBottom: 6 }}>
                핵심 인용
              </div>
              <ul
                className="list-reset"
                style={{ display: 'flex', flexDirection: 'column', gap: 6, marginBottom: 14 }}
              >
                {mutation.data.quotes.map((q, i) => (
                  <li
                    key={i}
                    style={{
                      padding: '8px 12px',
                      background: 'var(--bg-elev-2)',
                      border: '1px solid var(--border)',
                      borderRadius: 8,
                      fontSize: 13,
                    }}
                  >
                    &ldquo;{q}&rdquo;
                  </li>
                ))}
              </ul>
            </>
          )}

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            <span className="pill">model: {mutation.data.model}</span>
            <span className="pill">in: {mutation.data.inputTokens}t</span>
            <span className="pill">out: {mutation.data.outputTokens}t</span>
            <span className="pill">{mutation.data.durationSec}s</span>
            <span className="pill pill--success">{mutation.data.workloadId}</span>
          </div>
        </div>
      )}
    </div>
  );
}
