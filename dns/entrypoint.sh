#!/bin/bash

while true
do
	# shellcheck disable=SC2016
	nc -l -p 31337 -c 'read message; getent hosts "$message" | cut -d" " -f1'
done
