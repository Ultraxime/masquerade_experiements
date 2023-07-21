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

	COUNTRY=${COUNTRY:-it}

	ID=$(stat -c "%u:%g" .)

	if [ -d /browsertime/browsertime-results ]; then
		mkdir -p /browsertime/archives/dumps
		chown -R $ID /browsertime/archives

		rsync --archive --exclude "archives" --exclude "results" --exclude "*.yml" --remove-source-files --progress /browsertime/browsertime-results/* /browsertime/archives/dumps

		# remove empty dir
		rsync --exclude "archives" --exclude "results" --exclude "*.yml" --delete --recursive --dirs --progress `mktemp -d`/ /browsertime/browsertime-results/
	fi

	if [ ! -f "/websites.txt" ]; then
		if $FULL_LIST; then
			cat /similarweb-2021.csv | awk -F , -v COUNTRY=$COUNTRY '$1 == COUNTRY' | cut -d, -f3 > /websites.txt
		else
			cp /$COUNTRY.txt /websites.txt
		fi
	fi
	
	OPTIONS="-b $BROWSER -n $ITERATIONS --video $VIDEO --prettyPrint --videoParams.convert false --skipHar "
	TOTAL=$(cat /websites.txt | wc -l)

	COUNT=1

	for website in $(cat /websites.txt)
	do
		echo -e "\n\nTesting $website ($COUNT/$TOTAL)\n"

		echo "Native Test"
	    /start.sh $OPTIONS https://www.$website
	    
	    echo -e "\nMasquerade Test"
	    /start.sh $OPTIONS --proxy.https $PROXY_MASQUERADE https://www.$website
	    
	    echo -e "\nSquid Test"
		/dns-client.sh $PROXY_SQUID | (read PROXY && \
		/start.sh $OPTIONS --proxy.https $PROXY https://www.$website)

		COUNT=$(($COUNT + 1))
	done

	exit 0
fi
