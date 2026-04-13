# syntax=docker/dockerfile:1.7

###
# Backend image — FastAPI served by uvicorn.
#
# Two-stage build: the first stage installs Python dependencies into a
# dedicated venv; the runtime stage copies only the venv and the source
# so the final image stays small.
###

FROM python:3.11-slim AS deps

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system deps if needed (kept minimal for now).
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt


FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH=/app

# Non-root user for the runtime.
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

COPY --from=deps /opt/venv /opt/venv
COPY app ./app

# Persistent data directory (mounted as a volume in docker-compose).
RUN mkdir -p /data && chown -R app:app /data
ENV WORKSTATION_DB_PATH=/data/workstation.db

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; \
sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/api/health',timeout=3).status==200 else 1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
