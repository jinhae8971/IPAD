interface Provider {
  id: string;
  name: string;
  description: string;
  envKey: string;
  status: '연결 대기' | '사용 가능' | '미설정';
  models: string[];
}

const PROVIDERS: Provider[] = [
  {
    id: 'anthropic',
    name: 'Anthropic',
    description: 'Claude 4.6 / 4.5 계열. 기본 프로바이더.',
    envKey: 'ANTHROPIC_API_KEY',
    status: '사용 가능',
    models: ['claude-opus-4-6', 'claude-sonnet-4-6', 'claude-haiku-4-5-20251001'],
  },
  {
    id: 'openai',
    name: 'OpenAI',
    description: 'GPT 계열. 보조 프로바이더.',
    envKey: 'OPENAI_API_KEY',
    status: '연결 대기',
    models: ['gpt-4o', 'gpt-4o-mini'],
  },
  {
    id: 'ollama',
    name: 'Local (Ollama)',
    description: '자체 호스팅 LLM. 오프라인 워크로드용.',
    envKey: 'OLLAMA_HOST',
    status: '미설정',
    models: ['llama3.1:8b', 'qwen2.5:14b'],
  },
];

function statusPillClass(status: Provider['status']) {
  if (status === '사용 가능') return 'pill pill--success';
  if (status === '연결 대기') return 'pill pill--warning';
  return 'pill pill--danger';
}

function maskKey(key: string) {
  return `${key} = ${'*'.repeat(8)}...${'*'.repeat(4)}`;
}

export default function ApiProviders() {
  return (
    <div className="page">
      <h2 className="page__title">API &amp; 프로바이더</h2>
      <p className="page__subtitle">
        워크스테이션이 사용할 LLM 프로바이더와 API 키를 관리합니다. 실제 시크릿은 환경 변수로
        주입됩니다.
      </p>

      <div className="grid grid--2">
        {PROVIDERS.map((p) => (
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
    </div>
  );
}
