FROM debian:stable-slim

LABEL maintainer "BRUNO Maxime <maxime.bruno@ens-lyon.fr>"

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY ./entrypoint.sh /

COPY ./dns-client.sh /

EXPOSE 31337

ENTRYPOINT ["/entrypoint.sh"]
