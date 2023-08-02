FROM debian:stable-slim

RUN apt-get update && apt-get install netcat-traditional

COPY ./entrypoint.sh /

COPY ./dns-client.sh /

EXPOSE 31337

ENTRYPOINT /entrypoint.sh
