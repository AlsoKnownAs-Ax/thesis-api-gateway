FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod 755 /install.sh && /install.sh && rm /install.sh

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app
COPY . .
RUN uv sync

ENV PATH="/app/.venv/bin:${PATH}"

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]