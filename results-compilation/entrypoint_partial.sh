#!/bin/bash
# -*- coding: utf-8 -*-
# @Author: Ultraxime
# @Last Modified by:   Ultraxime
# @Last Modified time: 2023-08-24 11:07:27
#
# This file is part of Masquerade experiements.
#
# Masquerade experiements is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or any later version.
#
# Masquerade experiements is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Masquerade experiements. If not, see <https://www.gnu.org/licenses/>.

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
