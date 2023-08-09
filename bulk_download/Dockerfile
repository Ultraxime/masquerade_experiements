FROM alpine

LABEL maintainer "BRUNO Maxime <maxime.bruno@ens-lyon.fr>"

RUN apk update \
	&& apk add \
		bash \
		curl \
		netcat-openbsd \
		rsync \
    && rm -rf /var/cache/apk/*

COPY --from=maximebruno/dns /dns-client.sh /

COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
