from python:3.12.4-slim

WORKDIR /app

COPY pyproject.toml .

RUN python3.12 -m pip install --upgrade pip &&\
    python3.12 -m pip install .

COPY . .

CMD ["startbot"]
