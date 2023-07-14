#!/bin/bash

for LOSS in 0 1 2 5; do

	for RTT in 0 10 20 50 100 200 500; do

		for BW in 40000 100 50 20 10 5 2 1; do

			echo "UPLOAD=$BW" > network.env
			echo "RTT=$RTT" >> network.env
			echo "LOSS=$LOSS" >> network.env

			make run
		done
	done
done

for TECHNOLOGY in 3g 4g; do

	for QUALITY in bad medium good; do

		echo "TECHNOLOGY=$TECHNOLOGY" > network.env
		echo "QUALITY=$QUALITY" >> network.env

		make run
	done
done

echo "OPERATOR=starlink" > network.env
echo "TECHNOLOGY=leosat" >> network.env
make run

echo "TECHNOLOGY=geosat" > network.env
make run

make full_compile