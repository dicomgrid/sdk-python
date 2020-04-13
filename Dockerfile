FROM python:3.7-alpine3.10

## Prepare poetry

# For building poetry (this is about 140 mb of deps)
# Gcc and clibs used by ambra-sdk requirements
RUN apk add --no-cache gcc musl-dev && \
    apk add --no-cache --virtual .build-deps \
        libffi-dev openssl-dev

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Clear system deps
RUN apk del .build-deps

## Prepare dependencies

# Copy only requirements to cache them in docker layer
WORKDIR /src
COPY poetry.lock pyproject.toml /src/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /src

# Build image
# docker build -t ambra_sdk .
# Run flake
# docker run ambra_sdk poetry run flake8
# Run mypy
# docker run ambra_sdk poetry run mypy ambra
# Run pytest
# docker run  --mount type=bind,source=path_to .secrets.toml,target=/src/.secrets.toml --mount type=bind,source=/etc/hosts,target=/etc/hosts ambra_sdk poetry run pytest
