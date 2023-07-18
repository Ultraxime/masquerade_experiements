"""
Module for the browsertime results
"""

import json
import os
import time

from typing import List, Dict

import yaml


class Report:
    """
    This class describes the result of one run of browsertime.
    """
    _page_load_time: List[int]
    _speed_index: List[int]

    def __init__(self, filename: str):
        self._page_load_time = []
        self._speed_index = []

        try:
            with open(filename+"/browsertime.json", "r", encoding="utf-8") as file:
                content = json.load(file)

            for attempt in content[0]["browserScripts"]:
                self._page_load_time.append(attempt["timings"]["pageTimings"]["pageLoadTime"])
            for attempt in content[0]["visualMetrics"]:
                self._speed_index.append(attempt["SpeedIndex"])
        except FileNotFoundError:
            pass

    def get_page_load_time(self) -> List[int]:
        """
        Gets the page load time.

        :returns:   The page load time.
        :rtype:     int list
        """
        return self._page_load_time

    def get_speed_index(self) -> List[int]:
        """
        Gets the speed index.

        :returns:   The speed index.
        :rtype:     int list
        """
        return self._speed_index


class BrowserTime:
    """
    This class describes the result of one run of the browsertime experiment.
    """
    _native: Dict[str, Report]
    _masquerade: Dict[str, Report]
    _squid: Dict[str, Report]

    def __init__(self, folder: str = "."):
        self._native = {}
        self._masquerade = {}
        self._squid = {}

        for website in os.scandir(folder):
            if website.name not in ("archives", "results") and website.is_dir():
                attempts = list(os.scandir(website.path))
                assert len(attempts) == 3
                attempts.sort(key=lambda f: f.path)
                self._native[website.name] = Report(attempts[0].path)
                self._masquerade[website.name] = Report(attempts[1].path)
                self._squid[website.name] = Report(attempts[2].path)

    def save(self):
        """
        Save the object as a yaml file
        """
        with open(f'/results/results/browsertime {time.asctime()}.yml',
                  "w", encoding="utf-8") as file:
            yaml.dump(self, file)

    def get_page_load_time(self) -> Dict[str, List[int]]:
        """
        Gets the page load time.
        
        :returns:   The page load time.
        :rtype:     str * (int List) dict
        """
        res = {"native": [],
               "masquerade" : [],
               "squid": []}
        for website, native in self._native.items():
            if (website in self._masquerade and website in self._squid
                and len(native.get_page_load_time())
                    == len(self._masquerade[website].get_page_load_time())
                and len(native.get_page_load_time())
                    == len(self._squid[website].get_page_load_time())):

                res["native"].extend(native.get_page_load_time())
                res["masquerade"].extend(self._masquerade[website].get_page_load_time())
                res["squid"].extend(self._squid[website].get_page_load_time())
        return res

    def get_speed_index(self) -> Dict[str, List[int]]:
        """
        Gets the speed index.
        
        :returns:   The speed index.
        :rtype:     str * (int List) dict
        """
        res = {"native": [],
               "masquerade" : [],
               "squid": []}
        for website, native in self._native.items():
            if (website in self._masquerade and website in self._squid
                and len(native.get_speed_index())
                    == len(self._masquerade[website].get_speed_index())
                and len(native.get_speed_index()) == len(self._squid[website].get_speed_index())):

                res["native"].extend(native.get_speed_index())
                res["masquerade"].extend(self._masquerade[website].get_speed_index())
                res["squid"].extend(self._squid[website].get_speed_index())
        return res
