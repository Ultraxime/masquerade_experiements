#!/bin/bash

ID=$(stat -c "%u:%g" /results)

if [ -n "$TECHNOLOGY" ]; then
	OPERATOR=${OPERATOR:-"universal"}
	COUNTRY=${COUNTRY:-"universal"}
	QUALITY=${QUALITY:-"universal"}
	DIR=$(find /results/archives/ -iname "*$OPERATOR $COUNTRY $TECHNOLOGY $QUALITY*" -maxdepth 1 | tail -n 1)
else
	DOWNLOAD=${DOWNLOAD:-$UPLOAD}
	UPLOAD="$UPLOAD"000
	DOWNLOAD="$DOWNLOAD"000
	DIR=$(find /results/archives/ -iname "*$UPLOAD $DOWNLOAD $RTT $LOSS*" -maxdepth 1 | tail -n 1)
fi


if [ ! -d /results/browsertime-results ]; then
	if [ -z "$DIR" ]; then
		exit
	fi
	rsync --archive "$DIR"/* /results
fi


mkdir -p /results/results
if [ -n "$TECHNOLOGY" ]; then
	python /compile_partial.py -o "$OPERATOR" -c "$COUNTRY" -t "$TECHNOLOGY" -q "$QUALITY"

	DIR="/results/archives/$OPERATOR $COUNTRY $TECHNOLOGY $QUALITY $(date -Iseconds)"

else
	python /compile_partial.py -u "$UPLOAD" -d "$DOWNLOAD" -r "$RTT" -l "$LOSS"

	DIR="/results/archives/$UPLOAD $DOWNLOAD $RTT $LOSS $(date -Iseconds)"
fi

mkdir -p "$DIR"
chown -R "$ID" /results/archives

rsync --archive --exclude "archives" --exclude "results" --include "*/" --include "**/browsertime.json" --include '*.yml' --exclude "*" --prune-empty-dirs --remove-source-files /results/* "$DIR"

# remove empty dir
rsync --exclude "archives" --exclude "results" --delete --recursive "$(mktemp -d)"/ /results/

chown -R "$ID" /results/results
