# First, build the application in the `/app` directory.
# See `Dockerfile` for details.
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /venv

RUN apt-get update && apt-get install -y libpq-dev gcc && apt-get clean

RUN --mount=type=cache,id=uv-cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
ADD pyproject.toml pyproject.toml
ADD uv.lock uv.lock
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# Then, use a final image without uv
FROM python:3.12-slim-bookworm
# It is important to use the image that matches the builder, as the path to the
# Python executable must be the same, e.g., using `python:3.11-slim-bookworm`
# will fail.

# Copy the application from the builder
COPY --from=builder --chown=venv:venv /venv /venv

# Place executables in the environment at the front of the path
ENV PATH="/venv/.venv/bin:$PATH"
WORKDIR /app
COPY . .

EXPOSE 8000

# Comando por defecto para ejecutar la API con uv
# CMD ["fastapi", "dev", "src/main.py"]
