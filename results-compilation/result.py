import os
import yaml
import matplotlib.pyplot as plt
import time

from typing import List


class Result:
    _proxy: List
    _no_proxy: List

    def __init__(self, folder: str = ".", name: str = None):
        for file in os.scandir(folder):
            if not file.is_dir() and name in file.name:
                with open(file.path, "r", encoding="utf-8") as f:
                    content = yaml.safe_load(f)

        self._proxy = content["proxy"]
        self._no_proxy = content["no-proxy"]

    def subplot(self, name: str, unit: str = None, convert = lambda x: [float(x)], scale="linear"):
        proxy = []
        for test in self._proxy:
            proxy.extend(convert(test))
        proxy.sort()
        
        no_proxy = []
        for test in self._no_proxy:
            no_proxy.extend(convert(test))
        no_proxy.sort()
        
        proxy_length = len(proxy)
        no_proxy_length = len(no_proxy)

        # fig, ax = plt.subplots()

        plt.plot(proxy, [(i+1)/proxy_length for i in range(proxy_length)], label="proxied (%s tests)" % proxy_length)
        plt.plot(no_proxy, [(i+1)/no_proxy_length for i in range(no_proxy_length)], label="native (%s tests)" % no_proxy_length)

        plt.axis([min(proxy[0], no_proxy[0]), max(proxy[-1], no_proxy[-1]),
                  0, 1])
        plt.ylabel('ECDF')
        plt.xlabel('%s' % name + ((" (%s)" % unit) if unit else ""))
        plt.xscale(scale)

        plt.legend(loc="lower right")

        plt.savefig('/results/results/%s %s.png' % (name, time.asctime()))
        plt.clf()

    def plot(self):
        self.subplot(type(self).__name__)

    