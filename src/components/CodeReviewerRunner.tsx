import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { runCodeReviewer, type CodeReviewerResponse, type ReviewSeverity } from '../api/runs';

const severityPill: Record<ReviewSeverity, string> = {
  critical: 'pill pill--danger',
  warning: 'pill pill--warning',
  info: 'pill',
};

interface RunArgs {
  diff: string;
  context: string;
}

/**
 * Run panel embedded in the Code Reviewer agent detail view.
 *
 * POSTs a unified diff (and optional context) to
 * /api/agents/code-reviewer/run and renders the resulting comments
 * ordered by severity. Invalidates the workloads query on success.
 */
export default function CodeReviewerRunner() {
  const [diff, setDiff] = useState('');
  const [context, setContext] = useState('');
  const queryClient = useQueryClient();

  const mutation = useMutation<CodeReviewerResponse, Error, RunArgs>({
    mutationFn: ({ diff: d, context: c }) =>
      runCodeReviewer({ diff: d, context: c ? c : undefined }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workloads'] });
    },
  });

  const canRun = diff.trim().length > 0 && !mutation.isPending;

  return (
    <div style={{ marginTop: 20 }}>
      <div className="kv__k" style={{ marginBottom: 8 }}>
        실행
      </div>

      <label className="kv__k" htmlFor="cr-diff" style={{ display: 'block', marginBottom: 6 }}>
        Diff (unified)
      </label>
      <textarea
        id="cr-diff"
        value={diff}
        onChange={(e) => setDiff(e.target.value)}
        placeholder="git diff 결과를 붙여넣으세요 (unified diff)"
        aria-label="리뷰할 diff"
        rows={8}
        style={{
          width: '100%',
          padding: '10px 12px',
          background: 'var(--bg-elev-2)',
          border: '1px solid var(--border)',
          borderRadius: 8,
          color: 'var(--text)',
          fontFamily: 'SFMono-Regular, Menlo, monospace',
          fontSize: 12.5,
          resize: 'vertical',
        }}
      />

      <label
        className="kv__k"
        htmlFor="cr-context"
        style={{ display: 'block', marginTop: 10, marginBottom: 6 }}
      >
        Context (선택)
      </label>
      <textarea
        id="cr-context"
        value={context}
        onChange={(e) => setContext(e.target.value)}
        placeholder="PR 설명, 관련 이슈 번호 등"
        aria-label="리뷰 컨텍스트"
        rows={2}
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
          onClick={() => mutation.mutate({ diff, context })}
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
          {mutation.isPending ? '실행 중...' : 'Run Code Reviewer'}
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

          {mutation.data.comments.length > 0 ? (
            <>
              <div className="kv__k" style={{ marginBottom: 6 }}>
                코멘트 ({mutation.data.comments.length})
              </div>
              <ul
                className="list-reset"
                style={{ display: 'flex', flexDirection: 'column', gap: 8, marginBottom: 14 }}
              >
                {mutation.data.comments.map((c, i) => (
                  <li
                    key={`${c.file}-${c.line}-${i}`}
                    style={{
                      padding: '10px 12px',
                      background: 'var(--bg-elev-2)',
                      border: '1px solid var(--border)',
                      borderRadius: 8,
                      fontSize: 13,
                    }}
                  >
                    <div
                      style={{
                        display: 'flex',
                        gap: 8,
                        alignItems: 'center',
                        marginBottom: 4,
                      }}
                    >
                      <span className={severityPill[c.severity]}>{c.severity}</span>
                      <code style={{ color: 'var(--text-muted)', fontSize: 12 }}>
                        {c.file}:{c.line}
                      </code>
                    </div>
                    <div>{c.message}</div>
                  </li>
                ))}
              </ul>
            </>
          ) : (
            <p className="muted">모델이 반환한 코멘트가 없습니다.</p>
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
