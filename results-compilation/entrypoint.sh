#!/bin/bash

ID=$(stat -c "%u:%g" /results)

mkdir -p /results/results
python /compile.py
chown -R $ID /results/results
