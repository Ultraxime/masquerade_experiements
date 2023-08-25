#!/bin/bash
# -*- coding: utf-8 -*-
# @Author: Ultraxime
# @Last Modified by:   Ultraxime
# @Last Modified time: 2023-08-24 11:07:32
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

run(){
	echo "UPLOAD=$1" > network.env
	echo "RTT=$2" >> network.env
	echo "LOSS=$3" >> network.env

	make run
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

		make run
	done
done

echo "OPERATOR=starlink" > network.env
echo "TECHNOLOGY=leosat" >> network.env
make run

echo "TECHNOLOGY=geosat" > network.env
make run

make full_compile
