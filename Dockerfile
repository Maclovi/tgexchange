from python:3.12.4-slim

WORKDIR /app

COPY . .

RUN python3.12 -m pip install --upgrade pip &&\
    python3.12 -m pip install .

CMD ["startbot"]
