#!/bin/bash

# Normally already set to 1 but better be sure for the futur
if [ "$(cat /proc/sys/net/ipv4/ip_forward)" != "1" ]; then
	echo 1 > /proc/sys/net/ipv4/ip_forward
fi

iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

ip route

sleep infinity