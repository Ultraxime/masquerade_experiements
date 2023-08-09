ARG type

FROM debian:stable-slim AS base

LABEL maintainer "BRUNO Maxime <maxime.bruno@ens-lyon.fr>"

WORKDIR /usr/src

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libglib2.0-0 \
        libnss3 \
    && rm -rf /var/lib/apt/lists/*

COPY lib/* .


FROM base AS server

COPY certs certs

COPY masque_server .

COPY server.sh .

ENV proxy_port=1024

ENTRYPOINT ["./server.sh"]


FROM base AS client

COPY masque_client .

COPY client.sh .

ENV proxy_addr=localhost:1024
ENV website=www.google.com

ENTRYPOINT ["./client.sh"]


FROM ${type}
