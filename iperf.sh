#!/bin/bash

run(){
	echo "UPLOAD=$1" > network.env
	echo "RTT=$2" >> network.env
	echo "LOSS=$3" >> network.env

	docker compose -f docker-compose-iperf.yml run --remove-orphans iperf-client
}

for BW in 40000 100 50 20 10 5 2 1; do
	run "$BW" 0 0
done

for LOSS in 1 2 5; do
	run 100 0 "$LOSS"
done

for RTT in 10 20 50 100 200 500; do
	run 100 "$RTT" 0
done

for TECHNOLOGY in 3g 4g; do

	for QUALITY in bad medium good; do

		echo "TECHNOLOGY=$TECHNOLOGY" > network.env
		echo "QUALITY=$QUALITY" >> network.env

		docker compose -f docker-compose-iperf.yml run --remove-orphans iperf-client
	done
done

echo "OPERATOR=starlink" > network.env
echo "TECHNOLOGY=leosat" >> network.env
docker compose -f docker-compose-iperf.yml run --remove-orphans iperf-client

echo "TECHNOLOGY=geosat" > network.env
docker compose -f docker-compose-iperf.yml run --remove-orphans iperf-client
