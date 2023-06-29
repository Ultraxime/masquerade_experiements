import yaml
import json
import os
import matplotlib.pyplot as plt
import time

from result import Result

from typing import List, Tuple, Dict


class Report:
    pageLoadTime: List[int]

    def __init__(self, filename: str):
        self.pageLoadTime = []
        
        try:
            with open(filename+"/browsertime.json", "r", encoding="utf-8") as file:
                content = json.load(file)
            
            for attempt in content[0]["browserScripts"]:
                self.pageLoadTime.append(attempt["timings"]["pageTimings"]["pageLoadTime"])
        except FileNotFoundError:
            pass

    def __repr__(self):
        return self.pageLoadTime.__repr__()


class BrowserTime(Result):
    _proxy: List[Tuple[str, Report]]
    _no_proxy: List[Tuple[str, Report]]

    def __init__(self, folder: str = "."):
        self._no_proxy = []
        self._proxy = []

        for website in os.scandir(folder):
            if website.name not in ("archives", "results") and website.is_dir():
                attempts = [attempt for attempt in os.scandir(website.path)]
                assert len(attempts) == 2
                attempts.sort(key=lambda f: f.path)
                self._no_proxy.append((website.name, Report(attempts[0].path)))
                self._proxy.append((website.name, Report(attempts[1].path)))

    def plot(self):
        self.subplot("Page Load Time", "ms", lambda x : [int(test) for test in x[1].pageLoadTime])

    def save(self):
        with open('/results/results/browsertime %s.yml' % time.asctime(), "w", encoding="utf-8") as file:
            yaml.dump(self, file)