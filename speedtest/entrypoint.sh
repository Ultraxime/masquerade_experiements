#!/bin/bash

MESURE=${MESURE:-true}


function network_setup {

	GATEWAY=${GATEWAY:-gateway}

	# ip route

	GATEWAY_IP=$(getent hosts $GATEWAY | cut -d" " -f1 | head -n 1)
	# echo $GATEWAY_IP
	ip route delete default
	ip route add default via $GATEWAY_IP dev eth0

	# ip route
}


if $MESURE; then
	
	network_setup

	BROWSER=${BROWSER:-firefox}

	ITERATIONS=${ITERATIONS:-3}
	
	ID=$(stat -c "%u:%g" /results)

	if [ -e /results/speedtest*.yml ]; then
		mkdir -p /results/archives
		chown $ID /results/archives

		rsync --archive --remove-source-files --progress /results/speedtest*.yml /results/archives
	fi

	export FILE="/results/speedtest $(date).yml"
	touch "$FILE"

	/speedtest.py -n $ITERATIONS -b $BROWSER --name native
	
	/speedtest.py -n $ITERATIONS -x $PROXY_MASQUERADE -b $BROWSER --name proxy-masquerade
	
	/dns-client.sh $PROXY_SQUID | (read PROXY && \
	/speedtest.py -n $ITERATIONS -x $PROXY -b $BROWSER --name proxy-squid)

	chown -R $ID "$FILE"
fi
