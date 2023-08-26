FROM --platform=amd64 python:3.11-slim-buster

WORKDIR /app

COPY app/ /app

RUN pip install pdm

COPY pdm.lock pyproject.toml ./
RUN pdm sync

EXPOSE 8000

CMD ["pdm", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
