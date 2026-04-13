# AI Workstation Backend

FastAPI service that backs the AI Workstation web home.

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

OpenAPI docs: http://localhost:8000/docs

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Liveness + version |
| GET | `/api/agents/categories` | All agent categories |
| GET | `/api/agents` | All agents (optional `?category=coding`) |
| GET | `/api/agents/{id}` | Single agent |
| GET | `/api/providers` | LLM provider catalog |
| GET | `/api/workloads` | Current + recent workloads |

## Tests

```bash
cd backend
PYTHONPATH=. pytest
```
