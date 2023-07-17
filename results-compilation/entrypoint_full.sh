#!/bin/bash

ID=$(stat -c "%u:%g" /results)

mkdir -p /results/Loss /results/RTT /results/Download /results/Upload

python /compile.py

chown -R $ID /results
