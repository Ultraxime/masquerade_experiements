#!/bin/bash

# Normally already set to 1 but better be sure for the futur
if [ "$(cat /proc/sys/net/ipv4/ip_forward)" != "1" ]; then
	echo 1 > /proc/sys/net/ipv4/ip_forward
fi

# Internet
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Proxys
iptables -t nat -A POSTROUTING -o eth2 -j MASQUERADE


OPERATOR=${OPERATOR:-"universal"}
COUNTRY=${COUNTRY:-"universal"}
TECHNOLOGY=${TECHNOLOGY:-"3g"}
QUALITY=${QUALITY:-"medium"}
/errant -o $OPERATOR -c $COUNTRY -t $TECHNOLOGY -q $QUALITY -i eth2

ip addr

ip route

sleep infinity