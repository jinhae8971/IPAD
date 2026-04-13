import { useProviders, type Provider } from '../api/hooks';

function statusPillClass(status: Provider['status']) {
  if (status === '사용 가능') return 'pill pill--success';
  if (status === '연결 대기') return 'pill pill--warning';
  return 'pill pill--danger';
}

function maskKey(key: string) {
  return `${key} = ${'*'.repeat(8)}...${'*'.repeat(4)}`;
}

export default function ApiProviders() {
  const { data: providers, isLoading, isError } = useProviders();

  return (
    <div className="page">
      <h2 className="page__title">API &amp; 프로바이더</h2>
      <p className="page__subtitle">
        워크스테이션이 사용할 LLM 프로바이더와 API 키를 관리합니다. 실제 시크릿은 환경 변수로
        주입됩니다.
      </p>

      {isLoading && <p className="muted">프로바이더 불러오는 중...</p>}
      {isError && (
        <p className="muted">백엔드에 연결할 수 없어 프로바이더 목록을 표시할 수 없습니다.</p>
      )}

      {providers && providers.length > 0 && (
        <div className="grid grid--2">
          {providers.map((p) => (
            <div key={p.id} className="card">
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <strong style={{ fontSize: 15 }}>{p.name}</strong>
                <span className={statusPillClass(p.status)} style={{ marginLeft: 'auto' }}>
                  {p.status}
                </span>
              </div>
              <p className="muted" style={{ margin: '8px 0 12px' }}>
                {p.description}
              </p>
              <div className="kv" style={{ marginBottom: 10 }}>
                <span className="kv__k">환경 변수</span>
                <code className="kv__v">{maskKey(p.envKey)}</code>
              </div>
              <div className="kv">
                <span className="kv__k">모델</span>
                <div className="kv__v" style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                  {p.models.map((m) => (
                    <span key={m} className="pill">
                      {m}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
