#!/bin/bash
# -*- coding: utf-8 -*-
# @Author: Ultraxime
# @Last Modified by:   Ultraxime
# @Last Modified time: 2023-08-24 11:07:50
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

LOG_LEVEL=${LOG_LEVEL:-"info"}

DIR="/log/server"
mkdir -p "$DIR"
chmod 777 "$DIR"
export SSLKEYLOGFILE="$DIR/sslkeylog.log"
tcpdump port 4433 -w "$DIR/dump.pcap" &
RUST_BACKTRACE=1 RUST_LOG=$LOG_LEVEL /server "$SERVER"
