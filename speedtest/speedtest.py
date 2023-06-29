#!/usr/bin/env python3

from pyspeedtest import run_speedtest

import argparse
import json
import time
import yaml

parser = argparse.ArgumentParser(
                    prog='SpeedTest',
                    description='Perform a speedtest of the network',
                    epilog='')

parser.add_argument('-b', '--browser', default="firefox", nargs='?', required=False, type=str)
parser.add_argument('-n', '--iterations', default=1, nargs='?', required=False, type=int)
parser.add_argument('-x', '--proxy', default=None, nargs='?', required=False, type=str)

args = parser.parse_args()

proxy = []
no_proxy = []
for i in range(args.iterations):
	print("Test n°" + str(i))
	no_proxy.append(run_speedtest(browser=args.browser, pcap_path="trace.pcap", options=["--headless"]))
	if args.proxy:
		proxy.append(run_speedtest(browser=args.browser, pcap_path="trace.pcap", options=["--headless", '--proxy-server=%s' % args.proxy]))

print(proxy)
print(no_proxy)

with open('/results/speedtest %s.yml' % time.asctime(), "w", encoding="utf-8") as file:
    yaml.dump({"proxy": proxy,
       		   "no-proxy": no_proxy},
       		  file)

