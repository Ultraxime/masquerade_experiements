#!/bin/bash

MESURE=${MESURE:-true}

if $MESURE; then
	ITERATIONS=${ITERATIONS:-3}
	
	ID=$(stat -c "%u:%g" /results)

	if [ -e /results/bulk_download*.yml ]; then
		mkdir -p /results/archives
		chown $ID /results/archives

		echo archiving existing file

		rsync --archive --remove-source-files --progress /results/bulk_download*.yml /results/archives
	fi

	export FILE="/results/bulk_download $(date).yml"
	echo $FILE
	
	echo no-proxy: >> "$FILE"
	
	for i in $(seq 1 $ITERATIONS)
	do
		echo "Test n°$i (no_proxy)"
		echo -n "  - " >> "$FILE"
		curl -s -w %{speed_download} -o /dev/null http://speed.hetzner.de/1GB.bin >> "$FILE"
		echo "" >> "$FILE"
	done
	
	echo proxy: >> "$FILE"
	
	for i in $(seq 1 $ITERATIONS)
	do
		echo "Test n°$i (proxy)"
		echo -n "  - " >> "$FILE"
		curl -s -w %{speed_download} -o /dev/null -p -x $PROXY http://speed.hetzner.de/1GB.bin >> "$FILE"
		echo "" >> "$FILE"
	done
	
	chown -R $ID "$FILE"
fi
