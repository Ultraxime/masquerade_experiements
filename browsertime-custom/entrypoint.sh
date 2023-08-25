#!/bin/bash
# -*- coding: utf-8 -*-
# @Author: Ultraxime
# @Last Modified by:   Ultraxime
# @Last Modified time: 2023-08-24 11:07:44
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

MESURE=${MESURE:-true}


function network_setup {

	GATEWAY=${GATEWAY:-gateway}

	# ip route

	GATEWAY_IP=$(getent hosts "$GATEWAY" | cut -d" " -f1 | head -n 1)
	# echo $GATEWAY_IP
	ip route delete default
	ip route add default via "$GATEWAY_IP" dev eth0

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
		chown -R "$ID" /browsertime/archives

		rsync --archive --exclude "archives" --exclude "results" --exclude "*.yml" --include "*/" --include "**/browsertime.json" --exclude "*" --prune-empty-dirs --remove-source-files --progress /browsertime/browsertime-results/* /browsertime/archives/dumps

		# remove empty dir
		rsync --exclude "archives" --exclude "results" --exclude "*.yml" --delete --recursive --dirs --progress "$(mktemp -d)"/ /browsertime/browsertime-results/
	fi

	if [ ! -f "/websites.txt" ]; then
		if $FULL_LIST; then
			awk -F , -v COUNTRY="$COUNTRY" '$1 == COUNTRY' /similarweb-2021.csv | cut -d, -f3 > /websites.txt
		else
			cp /"$COUNTRY".txt /websites.txt
		fi
	fi

	OPTIONS=(-b "$BROWSER" -n "$ITERATIONS" --video "$VIDEO" --prettyPrint --videoParams.convert false --skipHar --videoParams.threads 16)
	TOTAL=$(wc -l /websites.txt | cut -d" " -f1)

	COUNT=1

	while IFS= read -r website
	do
		echo -e "\n\nTesting $website ($COUNT/$TOTAL)\n"

		echo "Native Test"
	    /start.sh "${OPTIONS[@]}" https://www."$website"

	    echo -e "\nMasquerade Test"
	    /start.sh "${OPTIONS[@]}" --proxy.https "$PROXY_MASQUERADE" https://www."$website"

	    echo -e "\nSquid Test"
		/dns-client.sh "$PROXY_SQUID" | (read -r PROXY && \
		/start.sh "${OPTIONS[@]}" --proxy.https "$PROXY" https://www."$website")

		COUNT=$((COUNT + 1))
	done < /websites.txt

	exit 0
fi
