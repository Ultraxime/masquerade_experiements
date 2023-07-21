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

	ITERATIONS=${ITERATIONS:-3}
	
	ID=$(stat -c "%u:%g" /results)

	if [ -e /results/bulk_download*.yml ]; then
		mkdir -p /results/archives/dumps
		chown -R $ID /results/archives

		echo archiving existing file

		rsync --archive --remove-source-files --progress /results/bulk_download*.yml /results/archives/dumps
	fi

	export FILE="/results/bulk_download $(date -Iseconds).yml"
	echo $FILE
	
	echo native: >> "$FILE"
	
	for i in $(seq 1 $ITERATIONS)
	do
		echo "Test n°$i (native)"
		echo -n "  - " >> "$FILE"
		curl -s -w %{speed_download} -o /dev/null http://speed.hetzner.de/1GB.bin >> "$FILE"
		echo "" >> "$FILE"
	done
	
	echo proxy-masquerade: >> "$FILE"
	
	for i in $(seq 1 $ITERATIONS)
	do
		echo "Test n°$i (proxy-masquerade)"
		echo -n "  - " >> "$FILE"
		curl -s -w %{speed_download} -o /dev/null -p -x $PROXY_MASQUERADE http://speed.hetzner.de/1GB.bin >> "$FILE"
		echo "" >> "$FILE"
	done
	
	echo proxy-squid: >> "$FILE"
	
	for i in $(seq 1 $ITERATIONS)
	do
		echo "Test n°$i (proxy-squid)"
		echo -n "  - " >> "$FILE"
		/dns-client.sh $PROXY_SQUID | (read PROXY && \
		curl -s -w %{speed_download} -o /dev/null -p -x $PROXY http://speed.hetzner.de/1GB.bin >> "$FILE")
		echo "" >> "$FILE"
	done
	
	chown -R $ID "$FILE"
fi
