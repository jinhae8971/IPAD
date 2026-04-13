import { Link, useParams } from 'react-router-dom';
import { useWorkload } from '../api/hooks';

function statusPillClass(status: string) {
  switch (status) {
    case 'running':
      return 'pill pill--warning';
    case 'success':
      return 'pill pill--success';
    case 'failed':
      return 'pill pill--danger';
    default:
      return 'pill';
  }
}

export default function WorkloadDetail() {
  const { workloadId } = useParams<{ workloadId: string }>();
  const { data: workload, isLoading, isError, error } = useWorkload(workloadId);

  return (
    <div className="page">
      <h2 className="page__title">워크로드 상세</h2>
      <p className="page__subtitle">
        <Link to="/workloads">← 목록으로</Link>
      </p>

      {isLoading && <p className="muted">불러오는 중...</p>}
      {isError && (
        <p className="muted">
          워크로드를 가져올 수 없습니다: {error?.message ?? '알 수 없는 오류'}
        </p>
      )}

      {workload && (
        <>
          <div className="card">
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <code style={{ fontSize: 14 }}>{workload.id}</code>
              <span className={statusPillClass(workload.status)}>{workload.status}</span>
              <span className="pill">{workload.agent}</span>
              <span className="pill" style={{ marginLeft: 'auto' }}>
                {workload.durationSec}s
              </span>
            </div>
            <p style={{ marginTop: 14, marginBottom: 0 }}>{workload.summary}</p>
            <div className="kv" style={{ marginTop: 12 }}>
              <span className="kv__k">시작</span>
              <span className="kv__v">{workload.startedAt}</span>
            </div>
          </div>

          <section className="page__section">
            <h3 className="page__section-title">결과</h3>
            {workload.result ? (
              <pre className="code-block" style={{ whiteSpace: 'pre-wrap', maxHeight: 480 }}>
                {JSON.stringify(workload.result, null, 2)}
              </pre>
            ) : workload.status === 'failed' ? (
              <p className="muted">실패한 워크로드입니다 — 결과가 없습니다.</p>
            ) : workload.status === 'running' || workload.status === 'queued' ? (
              <p className="muted">아직 결과가 기록되지 않았습니다.</p>
            ) : (
              <p className="muted">이 워크로드는 결과를 저장하지 않았습니다 (예: 시드 데이터).</p>
            )}
          </section>
        </>
      )}
    </div>
  );
}
