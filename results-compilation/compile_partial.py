"""
Compile the result of one experiment
"""

import argparse
import time
import yaml

from browsertime import BrowserTime
from bulktest import BulkTest
from speedtest import SpeedTest       # type: ignore [reportGeneralTypeIssues]

parser = argparse.ArgumentParser(
                    prog='compile',
                    description='Perform a speedtest of the network',
                    epilog='')

parser.add_argument('-t', '--technology', default=None, nargs='?', required=False, type=str)
parser.add_argument('-q', '--quality', default=None, nargs='?', required=False, type=str)
parser.add_argument('-o', '--operator', default=None, nargs='?', required=False, type=str)
parser.add_argument('-c', '--country', default=None, nargs='?', required=False, type=str)

parser.add_argument('-u', '--upload', default=None, nargs='?', required=False, type=int)
parser.add_argument('-d', '--download', default=None, nargs='?', required=False, type=int)
parser.add_argument('-r', '--rtt', default=None, nargs='?', required=False, type=int)
parser.add_argument('-l', '--loss', default=None, nargs='?', required=False, type=int)

args = parser.parse_args()

browsertime = BrowserTime("/results/browsertime-results")
speedTest = SpeedTest("/results")
bulkTest = BulkTest("/results")

if args.technology:
    with open(f"/results/results/{args.technology} {args.quality} "
              + f"{args.country} {args.operator} {time.asctime()}.yml",
              'w', encoding='utf8') as file:
        yaml.dump({"browsertime": browsertime,
                   "speedtest": speedTest,
                   "bulkTest": bulkTest},
                  file)
else:
    with open(f"/results/results/{args.upload} {args.download} "
              + f"{args.rtt} {args.loss} {time.asctime()}.yml",
              'w', encoding='utf8') as file:
        yaml.dump({"browsertime": browsertime,
                   "speedtest": speedTest,
                   "bulkTest": bulkTest},
                  file)
