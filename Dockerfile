# syntax=docker/dockerfile:1.7
# ---------------------------------------------------------------------------
# Etapa 1 · builder: resuelve dependencias con uv e instala el entorno
# ---------------------------------------------------------------------------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

COPY app ./app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# ---------------------------------------------------------------------------
# Etapa 2 · runtime: imagen mínima, usuario sin privilegios y volumen de datos
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    TECHDEV_DB_PATH=/app/data/app.db \
    TECHDEV_UPLOAD_DIR=/app/data/uploads

WORKDIR /app

RUN groupadd --system techdev \
    && useradd --system --gid techdev --home-dir /app --shell /usr/sbin/nologin techdev

COPY --from=builder --chown=techdev:techdev /app/.venv /app/.venv
COPY --chown=techdev:techdev app ./app

RUN mkdir -p /app/data/uploads && chown -R techdev:techdev /app/data

USER techdev

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import sys,urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4).status == 200 else 1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips=*"]
