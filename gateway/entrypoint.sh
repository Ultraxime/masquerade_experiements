#!/bin/bash
# -*- coding: utf-8 -*-
# @Author: Ultraxime
# @Last Modified by:   Ultraxime
# @Last Modified time: 2023-08-24 11:05:37
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

# Normally already set to 1 but better be sure for the futur
if [ "$(cat /proc/sys/net/ipv4/ip_forward)" != "1" ]; then
	echo 1 > /proc/sys/net/ipv4/ip_forward
fi

# Outside
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

if [ -n "$TECHNOLOGY" ]; then
	OPERATOR=${OPERATOR:-"universal"}
	COUNTRY=${COUNTRY:-"universal"}
	QUALITY=${QUALITY:-"universal"}
	PERIODIC=${PERIODIC:-10}
	/errant -o "$OPERATOR" -c "$COUNTRY" -t "$TECHNOLOGY" -q "$QUALITY" -i eth0 -p "$PERIODIC"
else
	DOWNLOAD=${DOWNLOAD:-$UPLOAD}
	UPLOAD="$UPLOAD"000
	DOWNLOAD="$DOWNLOAD"000
	/errant -u "$UPLOAD" -d "$DOWNLOAD" -R "$RTT" -L "$LOSS" -i eth0
fi

ip addr

ip route

sleep infinity
