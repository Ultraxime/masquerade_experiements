FROM python:3-alpine AS building_stage

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /usr/src

COPY requirements.txt .

RUN pip install -U --no-cache-dir --requirement requirements.txt


FROM python:3-alpine

LABEL maintainer "BRUNO Maxime <maxime.bruno@ens-lyon.fr>"

RUN apk update \
	&& apk add \
		bash \
		firefox \
		netcat-openbsd \
		rsync \
		tcpdump \
    && rm -rf /var/cache/apk/*

COPY --from=building_stage /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyspeedtest/pyspeedtest /pyspeedtest

COPY --from=maximebruno/dns /dns-client.sh /

COPY speedtest.py /

COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
