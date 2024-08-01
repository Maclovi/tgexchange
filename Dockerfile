from python:3.12.4-slim as builder

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
RUN uv pip install --no-cache --system .

COPY ./exchange ./.env .
RUN uv pip install --no-cache --system -e .
