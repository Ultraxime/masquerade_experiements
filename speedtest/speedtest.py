#!/usr/bin/env python3
"""
Module to realise a speed test
"""
import argparse
import os
from typing import Optional

import yaml
from pyspeedtest import run_speedtest # type: ignore [reportGeneralTypeIssues] # pylint: disable=no-name-in-module

def speedtest(data: list, browser: str, proxy: Optional[str] = None, count: int = 3):
    """
    run a Speedtest, with three try to prevent failures

    :param      data:     The data
    :type       data:     list
    :param      browser:  The browser
    :type       browser:  str
    :param      proxy:    The proxy
    :type       proxy:    the proxy to use
    :param      count:    The count
    :type       count:    int

    :returns:   Nothing
    :rtype:     NoneType
    """
    try:
        if proxy:
            print(proxy)
            data.append(run_speedtest(
                browser=browser,
                pcap_path="trace.pcap",
                options=["--headless", f"--proxy-server=\"{proxy}\""]))
        else:
            data.append(run_speedtest(
                browser=browser,
                pcap_path="trace.pcap",
                options=["--headless"]))
    except:                                                             # pylint: disable=bare-except
        if count == 0:
            return
        speedtest(data, browser, proxy, count-1)

parser = argparse.ArgumentParser(
                    prog='SpeedTest',
                    description='Perform a speedtest of the network',
                    epilog='')

parser.add_argument('-b', '--browser', default="firefox", nargs='?', required=False, type=str)
parser.add_argument('-n', '--iterations', default=1, nargs='?', required=False, type=int)
parser.add_argument('-x', '--proxy', default=None, nargs='?', required=False, type=str)
parser.add_argument('--name', default="native", nargs='?', required=False, type=str)

args = parser.parse_args()

content = None # pylint: disable=invalid-name

for file in os.scandir("/results"):
    if not file.is_dir() and "speedtest" in file.name:
        with open(file.path, "r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

            if not isinstance(content, dict):
                content = {}
            content[args.name] = []

            for i in range(args.iterations):
                print("Test n°" + str(i) + " (" + args.name + ")")
                speedtest(content[args.name], args.browser, args.proxy)

        with open(file.path, "w", encoding="utf-8") as file:
            yaml.dump(content, file)
