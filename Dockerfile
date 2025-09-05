FROM astral/uv:python3.13-bookworm

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY . .

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80