# FROM python:3.9-slim
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# ------------------------------------------------------------------------------

# SET version label
ARG BUILD_DATE=latest
ARG VERSION=0.0.1
LABEL build_version="MVladislav version:- ${VERSION} Build-date:- ${BUILD_DATE}"
LABEL maintainer="MVladislav"

# ------------------------------------------------------------------------------

# SET work dir
WORKDIR /app/

# GET all file
COPY ./ /app
RUN cp .env_template_kons .env

# ------------------------------------------------------------------------------

# SET project arguments
ARG ENV_MODE=KONS
ARG LOGGING_LEVEL=DEBUG
ARG LOGGING_VERBOSE=2

# ARG SECRET_KEY
RUN export SECRET_KEY=$(openssl rand -hex 64)

ARG DB_HOST=mongo
ARG DB_PORT=27017

# ------------------------------------------------------------------------------

# SET env
ENV DEBIAN_FRONTEND=noninteractive
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED=1

# SET env for is docker, used in setup script
ENV IS_DOCKER=true

# ------------------------------------------------------------------------------

# UPGRADE python pip
RUN python3 -m pip install --upgrade pip

# INSTALL
RUN python3 -m pip install .

# ------------------------------------------------------------------------------

ENV PATH=/root/.local/bin/:$PATH
ENV PYTHONPATH=/app:/usr/lib/python3/dist-packages/:$PYTHONPATH

# ------------------------------------------------------------------------------

# finish
EXPOSE $PORT
