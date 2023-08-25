#!/bin/bash
# -*- coding: utf-8 -*-
# @Author: Ultraxime
# @Last Modified by:   Ultraxime
# @Last Modified time: 2023-08-24 11:07:37
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

function run {
	count=3
	res=$($3)
	echo "$res"
	while [[ $res == 0 ]] && [[ $count -gt 0 ]]; do
		sleep 30
		res=$($3)
		echo "$res"
		count=$((count - 1))
	done
	if [[ $res != 0 ]]; then
		sed -i "s/$2:/$2:\n  - $res/" "$1"
	fi
}


if $MESURE; then

	network_setup

	ITERATIONS=${ITERATIONS:-3}

	ID=$(stat -c "%u:%g" /results)

	exist=$(ls /results/bulk_download*.yml)

	if [ -n "$exist" ]; then
		mkdir -p /results/archives/dumps
		chown -R "$ID" /results/archives

		echo archiving existing file

		rsync --archive --remove-source-files --progress /results/bulk_download*.yml /results/archives/dumps
	fi

	FILE="/results/bulk_download $(date -Iseconds).yml"
	echo "$FILE"

	echo native: > "$FILE"
	echo proxy-masquerade: >> "$FILE"
	echo proxy-squid: >> "$FILE"

	export OPTIONS="-s -w %{speed_download} -o /dev/null -m 60 "
	# export OPTIONS="-w %{speed_download} -o /dev/null -m 60 "

	for i in $(seq 1 "$ITERATIONS")
	do
		echo "Test n°$i/$ITERATIONS (native)"
		run "$FILE" "native" "curl $OPTIONS http://speed.hetzner.de/1GB.bin"

		echo "Test n°$i/$ITERATIONS (proxy-masquerade)"
		run "$FILE" "proxy-masquerade" "curl $OPTIONS -p -x $PROXY_MASQUERADE http://speed.hetzner.de/1GB.bin"

		echo "Test n°$i/$ITERATIONS (proxy-squid)"
		/dns-client.sh "$PROXY_SQUID" | (read -r PROXY && \
		run "$FILE" "proxy-squid" "curl $OPTIONS -p -x $PROXY http://speed.hetzner.de/1GB.bin")
		cat "$FILE"
	done

	chown -R "$ID" "$FILE"
fi
