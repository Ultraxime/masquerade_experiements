#!/bin/bash

ID=$(stat -c "%u:%g" /results)

mkdir -p /results/Loss /results/RTT /results/Download /results/Upload /results/Network /results/Bandwidth

python /compile.py

chown -R $ID /results
