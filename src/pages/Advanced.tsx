interface Feature {
  title: string;
  description: string;
  example: string;
}

const FEATURES: Feature[] = [
  {
    title: '훅 (Hooks)',
    description:
      '도구 호출 전/후, 세션 시작/종료 등 이벤트에 셸 명령을 연결합니다. 자동 린트, 커밋 검증, 노트 갱신 등에 활용.',
    example: `{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Edit|Write", "hooks": [{ "type": "command", "command": "npm run lint --silent" }] }
    ]
  }
}`,
  },
  {
    title: '스킬 (Skills)',
    description:
      '반복 작업을 담은 프롬프트·스크립트 묶음. 사용자가 /<skill>로 호출하거나 에이전트가 자동 선택.',
    example: `skills/
  commit/SKILL.md
  review-pr/SKILL.md
  simplify/SKILL.md`,
  },
  {
    title: 'MCP 서버',
    description:
      '외부 도구/데이터 소스를 Model Context Protocol로 연결합니다. GitHub, Slack, DB, 파일시스템 등.',
    example: `{
  "mcpServers": {
    "github": { "command": "github-mcp", "args": ["--repo", "jinhae8971/IPAD"] }
  }
}`,
  },
  {
    title: '서브에이전트',
    description:
      '특화된 역할(Explore, Plan, CodeReviewer 등)을 가진 에이전트를 병렬 실행하여 대용량 작업을 분산.',
    example: `Agent({
  subagent_type: "Plan",
  prompt: "Design the API surface for provider routing"
})`,
  },
];

export default function Advanced() {
  return (
    <div className="page">
      <h2 className="page__title">고급 기능</h2>
      <p className="page__subtitle">
        훅, 스킬, MCP 서버, 서브에이전트 등 바이브코딩 플랫폼을 확장하는 메커니즘.
      </p>

      <div className="grid grid--2">
        {FEATURES.map((f) => (
          <div key={f.title} className="card">
            <h3 style={{ marginTop: 0 }}>{f.title}</h3>
            <p className="muted">{f.description}</p>
            <pre className="code-block">{f.example}</pre>
          </div>
        ))}
      </div>
    </div>
  );
}
