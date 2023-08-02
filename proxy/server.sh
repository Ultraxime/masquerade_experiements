#!/bin/bash

LOG_LEVEL=${LOG_LEVEL:-"info"}

DIR="/log/server"
mkdir -p "$DIR"
chmod 777 "$DIR"
export SSLKEYLOGFILE="$DIR/sslkeylog.log"
tcpdump port 4433 -w "$DIR/dump.pcap" &
RUST_BACKTRACE=1 RUST_LOG=$LOG_LEVEL /server $SERVER
