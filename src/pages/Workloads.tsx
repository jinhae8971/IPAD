import { useWorkloads, type Workload } from '../api/hooks';

function statusPill(status: Workload['status']) {
  switch (status) {
    case 'running':
      return <span className="pill pill--warning">running</span>;
    case 'queued':
      return <span className="pill">queued</span>;
    case 'success':
      return <span className="pill pill--success">success</span>;
    case 'failed':
      return <span className="pill pill--danger">failed</span>;
  }
}

export default function Workloads() {
  const { data: workloads, isLoading, isError } = useWorkloads();

  return (
    <div className="page">
      <h2 className="page__title">워크로드</h2>
      <p className="page__subtitle">
        현재 실행 중인 작업과 최근 이력입니다. 15초마다 백엔드에서 자동 새로고침됩니다.
      </p>

      {isLoading && <p className="muted">워크로드 불러오는 중...</p>}
      {isError && <p className="muted">백엔드에 연결할 수 없어 워크로드를 가져올 수 없습니다.</p>}

      {workloads && workloads.length > 0 && (
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
            <thead>
              <tr style={{ background: 'var(--bg-elev-2)', textAlign: 'left' }}>
                <th style={{ padding: '10px 14px' }}>ID</th>
                <th style={{ padding: '10px 14px' }}>에이전트</th>
                <th style={{ padding: '10px 14px' }}>상태</th>
                <th style={{ padding: '10px 14px' }}>시작</th>
                <th style={{ padding: '10px 14px' }}>지속</th>
                <th style={{ padding: '10px 14px' }}>요약</th>
              </tr>
            </thead>
            <tbody>
              {workloads.map((w) => (
                <tr key={w.id} style={{ borderTop: '1px solid var(--border)' }}>
                  <td style={{ padding: '10px 14px', fontFamily: 'monospace' }}>{w.id}</td>
                  <td style={{ padding: '10px 14px' }}>{w.agent}</td>
                  <td style={{ padding: '10px 14px' }}>{statusPill(w.status)}</td>
                  <td style={{ padding: '10px 14px', color: 'var(--text-muted)' }}>
                    {w.startedAt}
                  </td>
                  <td style={{ padding: '10px 14px', color: 'var(--text-muted)' }}>
                    {w.durationSec}s
                  </td>
                  <td style={{ padding: '10px 14px' }}>{w.summary}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
