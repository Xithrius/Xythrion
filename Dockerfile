FROM --platform=linux/amd64 python:3.10-slim as poetry-base

# Disable pip cache and save poetry dependencies into system environment
ENV PIP_NO_CACHE_DIR=false \
    POETRY_VIRTUALENVS_CREATE=false

# Install poetry
RUN pip install -U poetry

# Create working directory
FROM poetry-base as csbot
WORKDIR /bot

# Install project dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install

# Copy source code
COPY . .
ENTRYPOINT ["python"]
CMD ["-m", "xythrion"]
