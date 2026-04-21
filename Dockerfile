FROM python:3.7.17-alpine3.18 as builder

ARG LIBRARYVERSION 0.0.1

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY dist/idplib-${LIBRARYVERSION}-py3-none-any.whl .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels idplib-${LIBRARYVERSION}-py3-none-any.whl
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels pytest

FROM python:3.7.17-alpine3.18

WORKDIR /app

COPY --from=builder /app/wheels /wheels

RUN pip install --no-cache /wheels/*

# Copy source code
COPY tests/ .


ENTRYPOINT [ "pytest", "/app" ]