FROM --platform=amd64 python:3.11 as builder

RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY pyproject.toml pdm.lock /project/
COPY app/ /project/app

WORKDIR /project
RUN mkdir __pypackages__ && pdm sync --prod --no-editable

FROM python:3.11

ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/__pypackages__/3.11/lib /project/pkgs

COPY --from=builder /project/__pypackages__/3.11/bin/* /bin/

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["alembic upgrade head && app.routers.application:get_app --host 0.0.0.0 --port 8001"]
