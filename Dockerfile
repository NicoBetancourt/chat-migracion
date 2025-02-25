# Primera fase: Construcción del entorno virtual con UV
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /venv

RUN apt-get update && apt-get install -y libpq-dev gcc && apt-get clean

# Copiar archivos an∫tes de instalar dependencias
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

# Segunda fase: Imagen final sin UV
FROM python:3.12-slim-bookworm

# Copiar el entorno virtual desde la imagen anterior
COPY --from=builder --chown=venv:venv /venv /venv

# Configurar el PATH para usar el entorno virtual
ENV PATH="/venv/.venv/bin:$PATH"
WORKDIR /app

# Crear un usuario sin privilegios para evitar problemas en Railway
RUN useradd -m streamlit_user
USER streamlit_user

# Copiar el código de la aplicación
COPY . .

ENV PORT=8000
EXPOSE ${PORT}

# Comando para ejecutar la API

# CMD ["sh", "-c", "fastapi dev src/main.py --host 0.0.0.0 --port ${PORT}"] # para fastapi
CMD ["sh", "-c", "streamlit run src/app.py --server.port=${PORT} --server.address=0.0.0.0"]

