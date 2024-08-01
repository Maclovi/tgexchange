from python:3.12.4-slim as builder

WORKDIR /app

COPY pyproject.toml .
RUN pip install uv && uv pip install --no-cache --system .

COPY ./exchange ./.env ./
RUN uv pip install --no-cache --system -e .

CMD ["startbot"]
