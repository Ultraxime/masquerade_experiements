#!/bin/bash

DNS=${DNS:-dns}
DNS_PORT=${DNS_PORT:-31337}

NAME=$(echo $1 | cut -d":" -f1)
PORT=$(echo $1 | cut -d":" -f2)

while true
do
	(echo $NAME | nc $DNS $DNS_PORT | (read IP && echo $IP:$PORT) 2>> /dns.log) && exit
done
