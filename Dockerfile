WORKDIR /app

COPY . .

RUN python3.12 -m pip install --upgrade pip &&\
    python3.12 -m pip install .

CMD ["startbot"]
# Build image to compile all packages
from python:3.12.4-slim as build

ENV VIRTUAL_ENV=/home/packages/.venv

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

COPY ./pyproject.toml .
RUN /root/.cargo/bin/uv venv /home/packages/.venv
RUN /root/.cargo/bin/uv pip install --no-cache --only-deps=.

FROM build

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    PATH="/home/packages/.venv/bin:$PATH" \
    VIRTUAL_ENV=/home/packages/.venv \
    PYTHONPATH="/home/app:$PYTHONPATH"

WORKDIR /app
COPY --from=build /home/packages/.venv /home/packages/.venv
COPY . .
