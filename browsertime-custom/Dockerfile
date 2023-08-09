FROM maximebruno/browsertime

LABEL maintainer "BRUNO Maxime <maxime.bruno@ens-lyon.fr>"

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		netcat-traditional \
		rsync \
	&& rm -rf /var/lib/apt/lists/*

COPY --from=maximebruno/dns /dns-client.sh /

COPY entrypoint.sh /entrypoint.sh

COPY similarweb-2021.csv de.txt fr.txt it.txt us.txt /

ENTRYPOINT ["/entrypoint.sh"]
