FROM python:3.11

WORKDIR /rest-api

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ../../../poetry.lock pyproject.toml ./

RUN poetry install --only main

COPY ../../src/ ./