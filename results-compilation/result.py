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

        self._masquerade = content["proxy-masquerade"]
        self._squid = content["proxy-squid"]
        self._native = content["native"]

    def develop(self, field, convert):
        res = []
        for test in field:
            res.extend(convert(test))
        res.sort()
        return res


    def subplot(self, name: str, unit: str = None, convert = lambda x: [float(x)], scale="linear"):
        mini = None
        maxi = None

        masquerade = self.develop(self._masquerade, convert)
        if masquerade != []:
            plt.plot(masquerade, [(i+1)/len(masquerade) for i in range(len(masquerade))], label="masquerade (%s tests)" % len(masquerade))
            mini = masquerade[0]
            maxi = masquerade[-1]
        

        squid = self.develop(self._squid, convert)
        if squid != []:
            plt.plot(squid, [(i+1)/len(squid) for i in range(len(squid))], label="squid (%s tests)" % len(squid))
            if mini:
                mini = min(mini, squid[0])
                maxi = max(maxi, squid[-1])
            else:
                mini = squid[0]
                maxi = squid[-1]
        
        native = self.develop(self._native, convert)
        if native != []:
            plt.plot(native, [(i+1)/len(native) for i in range(len(native))], label="native (%s tests)" % len(native))
            if mini:
                mini = min(mini, native[0])
                maxi = max(maxi, native[-1])
            else:
                mini = native[0]
                maxi = native[-1]
        
        plt.axis([mini, maxi, 0, 1])
        plt.ylabel('ECDF')
        plt.xlabel('%s' % name + ((" (%s)" % unit) if unit else ""))
        plt.xscale(scale)

        plt.legend(loc="lower right")

        plt.savefig('/results/results/%s %s.png' % (name, time.asctime()))
        plt.clf()

    def plot(self):
        self.subplot(type(self).__name__)

    