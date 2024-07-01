FROM --platform=amd64 python:3.12-slim as builder

RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY pyproject.toml pdm.lock /project/
COPY app/ /project/app

WORKDIR /project
RUN mkdir __pypackages__ && pdm sync --prod --no-editable

FROM python:3.12-slim

ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/__pypackages__/3.12/lib /project/pkgs

COPY --from=builder /project/__pypackages__/3.12/bin/* /bin/

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["cd api && alembic upgrade head && python3 -m app"]
