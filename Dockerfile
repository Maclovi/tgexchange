from python:3.12.4-slim as builder

WORKDIR /app

COPY . .

RUN pip install uv && uv pip install --no-cache --system -e .

CMD ["startbot"]
