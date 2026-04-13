interface Workload {
  id: string;
  agent: string;
  status: 'running' | 'queued' | 'success' | 'failed';
  startedAt: string;
  durationSec: number;
  summary: string;
}

const WORKLOADS: Workload[] = [
  {
    id: 'wl-0142',
    agent: 'Market Analyst',
    status: 'running',
    startedAt: '2026-04-13 09:00 KST',
    durationSec: 42,
    summary: '한미 증시 일일 리포트 생성 중',
  },
  {
    id: 'wl-0141',
    agent: 'Code Reviewer',
    status: 'queued',
    startedAt: '2026-04-13 08:58 KST',
    durationSec: 0,
    summary: 'PR #17 리뷰 대기',
  },
  {
    id: 'wl-0140',
    agent: 'Indexer',
    status: 'success',
    startedAt: '2026-04-13 08:30 KST',
    durationSec: 87,
    summary: '뉴스 임베딩 인덱스 갱신 완료',
  },
  {
    id: 'wl-0139',
    agent: 'Deployer',
    status: 'failed',
    startedAt: '2026-04-13 08:12 KST',
    durationSec: 19,
    summary: 'staging 헬스체크 실패 → 자동 롤백',
  },
];

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
  return (
    <div className="page">
      <h2 className="page__title">워크로드</h2>
      <p className="page__subtitle">
        현재 실행 중인 작업과 최근 이력입니다. (샘플 데이터 — 실제 백엔드 연동은 후속 단계)
      </p>

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
            {WORKLOADS.map((w) => (
              <tr key={w.id} style={{ borderTop: '1px solid var(--border)' }}>
                <td style={{ padding: '10px 14px', fontFamily: 'monospace' }}>{w.id}</td>
                <td style={{ padding: '10px 14px' }}>{w.agent}</td>
                <td style={{ padding: '10px 14px' }}>{statusPill(w.status)}</td>
                <td style={{ padding: '10px 14px', color: 'var(--text-muted)' }}>{w.startedAt}</td>
                <td style={{ padding: '10px 14px', color: 'var(--text-muted)' }}>
                  {w.durationSec}s
                </td>
                <td style={{ padding: '10px 14px' }}>{w.summary}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
