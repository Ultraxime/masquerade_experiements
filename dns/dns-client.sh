#!/bin/bash
# -*- coding: utf-8 -*-
# @Author: Ultraxime
# @Last Modified by:   Ultraxime
# @Last Modified time: 2023-08-24 11:07:00
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

DNS=${DNS:-dns}
DNS_PORT=${DNS_PORT:-31337}

NAME=$(echo "$1" | cut -d":" -f1)
PORT=$(echo "$1" | cut -d":" -f2)

while true
do
	(echo "$NAME" | nc "$DNS" "$DNS_PORT" | (read -r IP && echo "$IP":"$PORT") 2>> /dns.log) && exit
done
