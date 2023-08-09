ARG type

FROM python:3-alpine as building_stage

RUN apk update \
	&& apk add \
		g++ \
		jpeg-dev \
		libjpeg\
		make \
		zlib-dev \
    && rm -rf /var/cache/apk/*

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /usr/src/

COPY requirements.txt .

RUN pip install -U --no-cache-dir --requirement requirements.txt


FROM python:3-alpine as base

LABEL maintainer "BRUNO Maxime <maxime.bruno@ens-lyon.fr>"

RUN apk update \
	&& apk add \
		bash \
		libstdc++ \
		rsync \
    && rm -rf /var/cache/apk/*

COPY --from=building_stage /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY *.py /


FROM base as partial

COPY entrypoint_partial.sh /entrypoint.sh


FROM base as full

COPY entrypoint_full.sh /entrypoint.sh


FROM ${type}

ENTRYPOINT ["/entrypoint.sh"]
