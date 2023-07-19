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

/dns-client.sh $SERVER | (read SERVER_IP && echo $SERVER_IP && IP=$(echo $SERVER_IP | cut -d":" -f1) && \
iperf3 -c $IP)