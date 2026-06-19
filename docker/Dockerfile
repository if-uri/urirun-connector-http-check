FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
  && apt-get install -y --no-install-recommends bash ca-certificates curl git \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN python3 -m pip install --upgrade pip \
  && python3 -m pip install . \
  && python3 -m pip install "git+https://github.com/tellmesh/urirun.git@main#subdirectory=adapters/python"

CMD ["bash", "docker/run-smoke.sh"]
