#!/bin/bash

MESURE=${MESURE:-true}

if $MESURE; then
	BROWSER=${BROWSER:-firefox}

	ITERATIONS=${ITERATIONS:-3}
	
	ID=$(stat -c "%u:%g" /results)

	if [ -e /results/speedtest*.yml ]; then
		mkdir -p /results/archives
		chown $ID /results/archives

		rsync --archive --remove-source-files --progress /results/speedtest*.yml /results/archives
	fi

	/pyspeedtest/speedtest.py -n $ITERATIONS -x $PROXY -b $BROWSER

	chown -R $ID /results/speedtest*.yml
fi
