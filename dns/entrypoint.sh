#!/bin/bash

while true
do
	nc -l -p 31337 -c 'read message; getent hosts "$message" | cut -d" " -f1'
done
