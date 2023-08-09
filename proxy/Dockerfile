ARG type

FROM rust:alpine AS base

LABEL maintainer "BRUNO Maxime <maxime.bruno@ens-lyon.fr>"

RUN apk add --upgrade cmake build-base

WORKDIR /usr/src/
# RUN rustup target add x86_64-unknown-linux-musl

# COPY masquerade /tmp/masquerade

# RUN cargo new --lib masquerade

# WORKDIR masquerade
# RUN cp /tmp/masquerade/Cargo.toml .
# RUN cargo update
# RUN ls && sleep 30
# RUN cargo build --release

# RUN cp -r /tmp/masquerade/src .
# RUN cargo install --target x86_64-unknown-linux-musl --path .

# RUN ls /usr/local/cargo/bin && sleep 30

COPY masquerade/ masquerade

WORKDIR /usr/src/masquerade

RUN cargo fix --lib -p masquerade-proxy --allow-no-vcs \
    && cargo build --bins --release


FROM base AS client

RUN apk update \
    && apk add \
        bash \
        curl \
        iproute2 \
        netcat-openbsd \
        tcpdump \
    && rm -rf /var/cache/apk/*

ENV CLIENT=localhost:8989
ARG PORT=8989

EXPOSE ${PORT}

COPY --from=registry.ultraxime.fr/dns /dns-client.sh /

ENV healtcheck=https://www.google.com

HEALTHCHECK --interval=30s --timeout=1m --start-period=45s \
   CMD curl -f --retry 2 --max-time 15 --retry-delay 2 -p -x ${CLIENT} --head ${healtcheck} || bash -c 'kill -s 15 -1 && (sleep 10; kill -s 9 -1)'

COPY --from=base /usr/src/masquerade/target/release/client /client

COPY client.sh /client.sh

CMD ["/client.sh"]


FROM base AS server

ENV SERVER=localhost:4433
ARG PORT=4433

EXPOSE ${PORT}/udp

COPY --from=base /usr/src/masquerade/target/release/server /server

COPY server.sh /server.sh

RUN apk add tcpdump bash

CMD ["/server.sh"]


FROM ${type}
