#!/bin/bash

ID=$(stat -c "%u:%g" /results)

if [ -n "$TECHNOLOGY" ]; then
	OPERATOR=${OPERATOR:-"universal"}
	COUNTRY=${COUNTRY:-"universal"}
	QUALITY=${QUALITY:-"universal"}
	python /compile.py -o $OPERATOR -c $COUNTRY -t $TECHNOLOGY -q $QUALITY
else
	DOWNLOAD=${DOWNLOAD:-$UPLOAD}
	UPLOAD="$UPLOAD"000
	DOWNLOAD="$DOWNLOAD"000
	python /compile.py -u $UPLOAD -d $DOWNLOAD -r $RTT -l $LOSS
fi

chown -R $ID /results
