FROM python:3.8-slim
MAINTAINER L.Koné (loko-loko@github.com)

ENV PYTHONUNBUFFERED 1
WORKDIR /exporter

# Install bluetooth lib
RUN apt-get update \
    && apt-get install -y bluez \
    # Create temporary path
    && mkdir /tmp/.pkg

# Copy package + files
ADD mi_flower_exporter /tmp/.pkg/mi_flower_exporter
ADD setup.py /tmp/.pkg
ADD entrypoint.sh .

# Install package
RUN pip install /tmp/.pkg && rm -fr /tmp/.pkg \
    && chmod +x /exporter/entrypoint.sh

# Run entrypoint
ENTRYPOINT ["/exporter/entrypoint.sh"]