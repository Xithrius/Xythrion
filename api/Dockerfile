FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install uv && \
    rye config --set-bool behavior.use-uv=true

RUN rye sync

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["cd api && alembic upgrade head && python3 -m app"]
