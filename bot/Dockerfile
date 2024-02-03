FROM --platform=amd64 python:3.11 as builder

RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY pyproject.toml pdm.lock /project/
COPY bot/ /project/bot

WORKDIR /project
RUN mkdir __pypackages__ && pdm sync --prod --no-editable

FROM python:3.11

ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/__pypackages__/3.11/lib /project/pkgs
COPY --from=builder /project/__pypackages__/3.11/bin/* /bin/

ENTRYPOINT ["python3", "-m"]
CMD ["bot"]
