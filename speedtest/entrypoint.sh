#!/bin/bash
# -*- coding: utf-8 -*-
# @Author: Ultraxime
# @Last Modified by:   Ultraxime
# @Last Modified time: 2023-08-24 11:07:41
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

	BROWSER=${BROWSER:-firefox}

	ITERATIONS=${ITERATIONS:-3}

	ID=$(stat -c "%u:%g" /results)

	exist=$(ls /results/speedtest*.yml)

	if [ -n "$exist" ]; then
		mkdir -p /results/archives/dumps
		chown -R "$ID" /results/archives

		rsync --archive --remove-source-files --progress /results/speedtest*.yml /results/archives/dumps
	fi

	FILE="/results/speedtest $(date -Iseconds).yml"
	touch "$FILE"

	/speedtest.py -n "$ITERATIONS" -b "$BROWSER" --name native

	/speedtest.py -n "$ITERATIONS" -x "$PROXY_MASQUERADE" -b "$BROWSER" --name proxy-masquerade

	/dns-client.sh "$PROXY_SQUID" | (read -r PROXY && \
	/speedtest.py -n "$ITERATIONS" -x "$PROXY" -b "$BROWSER" --name proxy-squid)

	chown -R "$ID" "$FILE"
fi
