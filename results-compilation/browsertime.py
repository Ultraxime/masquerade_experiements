import yaml
import json
import os
import matplotlib.pyplot as plt
import time

from result import Result

from typing import List, Tuple, Dict


class Report:
    pageLoadTime: List[int]
    speedIndex: List[int]

    def __init__(self, filename: str):
        self.pageLoadTime = []
        self.speedIndex = []
        
        try:
            with open(filename+"/browsertime.json", "r", encoding="utf-8") as file:
                content = json.load(file)
            
            for attempt in content[0]["browserScripts"]:
                self.pageLoadTime.append(attempt["timings"]["pageTimings"]["pageLoadTime"])
            for attempt in content[0]["visualMetrics"]:
                self.speedIndex.append(attempt["SpeedIndex"])
        except FileNotFoundError:
            pass


class BrowserTime(Result):
    _proxy: List[Tuple[str, Report]]
    _no_proxy: List[Tuple[str, Report]]

    def __init__(self, folder: str = "."):
        self._native = []
        self._masquerade = []
        self._squid = []

        for website in os.scandir(folder):
            if website.name not in ("archives", "results") and website.is_dir():
                attempts = [attempt for attempt in os.scandir(website.path)]
                assert len(attempts) == 3
                attempts.sort(key=lambda f: f.path)
                self._native[website.name] = Report(attempts[0].path)
                self._masquerade[website.name] = Report(attempts[1].path)
                self._squid[website.name] = Report(attempts[2].path)

    def plot(self):
        self.subplot("Page Load Time", "ms", lambda x : [int(test) for test in x[1].pageLoadTime])
        self.subplot("Speed Index", "ms", lambda x : [int(test) for test in x[1].speedIndex])
        for website, test in self._masquerade:
            if test != []:
                self.subplot("Page Load Time %s" % website, "ms", lambda x : [int(test) for test in x[1].pageLoadTime] if x[0] == website else [])
                self.subplot("Speed Index %s" % website, "ms", lambda x : [int(test) for test in x[1].speedIndex] if x[0] == website else [])

    def save(self):
        with open('/results/results/browsertime %s.yml' % time.asctime(), "w", encoding="utf-8") as file:
            yaml.dump(self, file)
