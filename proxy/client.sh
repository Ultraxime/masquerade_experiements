#!/bin/bash

function network_setup {

    GATEWAY=${GATEWAY:-gateway}

    ip route

    GATEWAY_IP=$(getent hosts $GATEWAY | cut -d" " -f1 | head -n 1)
    echo $GATEWAY_IP
    ip route delete default
    ip route add default via $GATEWAY_IP dev eth0

    ip route
}

network_setup

SERVER=${SERVER:-"proxy-server:4433"}

CLIENT_TYPE=${CLIENT_TYPE:-"http"}

LOG_LEVE=${LOG_LEVEL:-"warn"}


/dns-client.sh $SERVER | (read SERVER_IP && echo $SERVER_IP && \
RUST_BACKTRACE=1 RUST_LOG=$LOG_LEVEL /client $SERVER_IP $CLIENT $CLIENT_TYPE)