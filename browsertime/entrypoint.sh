#!/bin/bash

MESURE=${MESURE:-true}

if $MESURE; then
	BROWSER=${BROWSER:-chrome}

	ITERATIONS=${ITERATIONS:-3}

	VIDEO=${VIDEO:-false}

	ID=$(stat -c "%u:%g" /browsertime/browsertime-results)

	if [ -d /browsertime/browsertime-results ]; then
		mkdir -p /browsertime/browsertime-results/archives
		chown $ID /browsertime/browsertime-results/archives

		rsync --archive --exclude "archives" --exclude "results" --exclude "*.yml" --remove-source-files --progress /browsertime/browsertime-results/* /browsertime/browsertime-results/archives

		# remove empty dir
		rsync --exclude "archives" --exclude "results" --exclude "*.yml" --delete --recursive --dirs --progress `mktemp -d`/ /browsertime/browsertime-results/
	fi

	for website in $(cat /websites.txt)
	do
	    /start.sh -b $BROWSER -n $ITERATIONS --video $VIDEO $website
	    /start.sh -b $BROWSER -n $ITERATIONS --video $VIDEO --proxy.https $PROXY $website
	done

	exit 0
fi
