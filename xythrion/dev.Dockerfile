FROM --platform=amd64 python:3.11-slim-buster

WORKDIR /bot

RUN apt update && apt install -y gcc

RUN pip install pdm

COPY pyproject.toml /bot
COPY pdm.lock /bot

RUN pdm install

COPY . /bot

CMD ["sh", "entrypoint.sh"]
