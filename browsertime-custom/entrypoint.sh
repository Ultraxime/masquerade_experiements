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

	BROWSER=${BROWSER:-chrome}

	ITERATIONS=${ITERATIONS:-3}

	VIDEO=${VIDEO:-false}

	FULL_LIST=${FULL_LIST:-false}

	COUNTRY=${COUNTRY:-fr}

	ID=$(stat -c "%u:%g" /browsertime/browsertime-results)

	if [ -d /browsertime/browsertime-results ]; then
		mkdir -p /browsertime/browsertime-results/archives
		chown $ID /browsertime/browsertime-results/archives

		rsync --archive --exclude "archives" --exclude "results" --exclude "*.yml" --remove-source-files --progress /browsertime/browsertime-results/* /browsertime/browsertime-results/archives

		# remove empty dir
		rsync --exclude "archives" --exclude "results" --exclude "*.yml" --delete --recursive --dirs --progress `mktemp -d`/ /browsertime/browsertime-results/
	fi

	if $FULL_LIST; then
		cat similarweb-2021.csv | awk -F , -v COUNTRY=$COUNTRY '$1 == COUNTRY' | cut -d, -f3 > /websites.txt
	else
		cp $COUNTRY.txt /websites.txt
	fi

	for website in $(cat /websites.txt)
	do
	    /start.sh -b $BROWSER -n $ITERATIONS --video $VIDEO https://www.$website
	    /dns-client.sh $PROXY_MASQUERADE | (read PROXY && echo $PROXY && \
		/start.sh -b $BROWSER -n $ITERATIONS --video $VIDEO --proxy.https $PROXY https://www.$website)
		/dns-client.sh $PROXY_SQUID | (read PROXY && echo $PROXY && \
		/start.sh -b $BROWSER -n $ITERATIONS --video $VIDEO --proxy.https $PROXY https://www.$website)
	done

	exit 0
fi