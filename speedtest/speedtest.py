#!/usr/bin/env python3

from pyspeedtest import run_speedtest

import argparse
import os
import yaml

parser = argparse.ArgumentParser(
                    prog='SpeedTest',
                    description='Perform a speedtest of the network',
                    epilog='')

parser.add_argument('-b', '--browser', default="firefox", nargs='?', required=False, type=str)
parser.add_argument('-n', '--iterations', default=1, nargs='?', required=False, type=int)
parser.add_argument('-x', '--proxy', default=None, nargs='?', required=False, type=str)
parser.add_argument('--name', default="native", nargs='?', required=False, type=str)

args = parser.parse_args()

content = None
for file in os.scandir("/results"):
    if not file.is_dir() and "speedtest" in file.name:
        with open(file.path, "r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

            if not isinstance(content, dict):
                content = {}
            content[args.name] = []

            for i in range(args.iterations):
                print("Test n°" + str(i) + " (" + args.name + ")")
                if args.proxy:
                    print(args.proxy)
                    content[args.name].append(run_speedtest(browser=args.browser, pcap_path="trace.pcap", options=["--headless", "--proxy-server=\"%s\"" % args.proxy]))
                else:
                    content[args.name].append(run_speedtest(browser=args.browser, pcap_path="trace.pcap", options=["--headless"]))

        with open(file.path, "w", encoding="utf-8") as file:
            yaml.dump(content, file)

        exit(0)

