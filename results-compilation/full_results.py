"""
Module for the result of the full experiment
"""
import os
import sqlite3
import time
from typing import Dict
from typing import Tuple

import fastplot
import pandas as pd
import yaml

# If up and download are correlated
BANDWIDTH = True


class Connectivity:
    """
    This class describes a connectivity.
    """
    _technology: int
    _quality: int

    def __init__(self, technology: str, quality: str = "universal"):
        match technology:
            case "leosat":
                self._technology = 0
            case "geosat":
                self._technology = 1
            case "3g":
                self._technology = 2
            case "4g":
                self._technology = 3
            case _:
                raise ValueError
        match quality:
            case "bad":
                self._quality = 0
            case "universal":
                self._quality = 1
            case "starlink":
                self._quality = 2
            case "medium":
                self._quality = 3
            case "good":
                self._quality = 4
            case _:
                raise ValueError

    def __eq__(self, other):
        if not isinstance(other, Connectivity):
            return False
        return self._technology == other._technology and self._quality == other._quality

    def __lt__(self, other):
        if not isinstance(other, Connectivity):
            return False
        return (self._technology < other._technology or
                (self._technology == other._technology and self._quality < other._quality))

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        match self._technology:
            case 0:
                name = "leosat"
            case 1:
                name = "geosat"
            case 2:
                name = "3g"
            case 3:
                name = "4g"
            case _:
                raise ValueError
        match self._quality:
            case 0:
                name += "\nbad"
            case 1:
                name += "\nuniversal"
            case 2:
                name += "\nstarlink"
            case 3:
                name += "\nmedium"
            case 4:
                name += "\ngood"
            case _:
                raise ValueError
        return name


class FullResults:
    """
    This class describes full results.
    """
    def __init__(self, folder: str = "."):
        self._connection = sqlite3.connect(f"{folder}/full_results {time.asctime()}.db")

        self._cursor = self._connection.cursor()
        self._cursor.execute("CREATE TABLE basic(upload, download, rtt, loss, data)")
        self._cursor.execute("CREATE TABLE errant(technology, quality, operator, country, data)")

        tests = list(os.scandir(folder))
        tests.sort(key=lambda f: f.path)

        for test in tests:
            if ".yml" in test.name:
                try:
                    self._add_basic(test)
                except ValueError:
                    self._add_errant(test)

    def _add_basic(self, test):
        data = test.name.split(" ")
        upload = int(data[0])//1000
        download = int(data[1])//1000
        rtt = int(data[2])
        loss = int(data[3])
        with open(test.path, 'r', encoding='utf-8') as file:
            data = file.read().encode("ascii", "replace")
            if self._cursor.execute(f"""SELECT * FROM basic
                                        WHERE upload={upload}
                                              AND download={download}
                                              AND rtt={rtt}
                                              AND loss={loss}""").fetchall() != []:
                self._cursor.execute(f"""UPDATE basic SET data=\"{data}\"
                                         WHERE upload={upload}
                                               AND download={download}
                                               AND rtt={rtt}
                                               AND loss={loss}""")
            else:
                self._cursor.execute(f"""INSERT INTO basic
                                         VALUES ({upload}, {download}, {rtt}, {loss},
                                                 \"{data}\")""")
            self._connection.commit()

    def _add_errant(self, test):
        data = test.name.split(" ")
        technology = data[0]
        quality = data[1]
        operator = data[2]
        country = data[3]
        with open(test.path, 'r', encoding='utf-8') as file:
            data = file.read().encode("ascii", "replace")
            if self._cursor.execute(f"""SELECT * FROM errant
                                        WHERE technology=\"{technology}\"
                                              AND quality=\"{quality}\"
                                              AND operator=\"{operator}\"
                                              AND country=\"{country}\"""").fetchall() != []:
                self._cursor.execute(f"""UPDATE errant SET data=\"{data}\"
                                         WHERE technology=\"{technology}\"
                                               AND quality=\"{quality}\"
                                               AND operator=\"{operator}\"
                                               AND country=\"{country}\"""")
            else:
                self._cursor.execute(f"""INSERT INTO errant
                                         VALUES (\"{technology}\",\"{quality}\", \"{operator}\", \"{country}\",
                                                 \"{data}\")""")
            self._connection.commit()

    # pylint: disable=too-many-branches
    def plot(self):
        """
        Create the graph for all the relevant data
        """
        for upload, download, rtt in self._cursor.execute("""SELECT DISTINCT upload, download, rtt
                                                             FROM basic""").fetchall():
            res = {}
            for loss, data in self._cursor.execute(f"""SELECT loss, data FROM basic
                                                       WHERE upload={upload}
                                                             AND download={download}
                                                             AND rtt={rtt}""").fetchall():
                data = yaml.load(data, Loader=yaml.Loader)
                res[loss] = data
            self.subplot(res, label="Loss", unit="%",
                         condition=f"upload: {upload}mbps download: {download}mbps, rtt: {rtt}ms")
        for upload, download, loss in self._cursor.execute("""SELECT DISTINCT upload, download, loss
                                                              FROM basic""").fetchall():
            res = {}
            for rtt, data in self._cursor.execute(f"""SELECT rtt, data FROM basic
                                                      WHERE upload={upload}
                                                            AND download={download}
                                                            AND loss={loss}""").fetchall():
                data = yaml.load(data, Loader=yaml.Loader)
                res[rtt] = data
            self.subplot(res, label="RTT", unit="ms",
                         condition=f"upload: {upload}mbps download: {download}mbps, loss: {loss}%")

        if BANDWIDTH:
            for rtt, loss in self._cursor.execute("""SELECT DISTINCT rtt, loss
                                                     FROM basic""").fetchall():
                res = {}
                for upload, data in self._cursor.execute(f"""SELECT upload, data FROM basic
                                                             WHERE rtt={rtt}
                                                                   AND loss={loss}""").fetchall():
                    data = yaml.load(data, Loader=yaml.Loader)
                    res[upload] = data
                self.subplot(res, label="Bandwidth", unit="mbps",
                             condition=f"rtt: {rtt}ms, loss: {loss}%")
        else:
            for upload, rtt, loss in self._cursor.execute("""SELECT DISTINCT upload, rtt, loss
                                                             FROM basic""").fetchall():
                res = {}
                for download, data in self._cursor.execute(f"""SELECT download, data FROM basic
                                                               WHERE upload={upload}
                                                                     AND rtt={rtt}
                                                                     AND loss={loss}""").fetchall():
                    data = yaml.load(data, Loader=yaml.Loader)
                    res[download] = data
                self.subplot(res, label="Download", unit="mbps",
                             condition=f"upload: {upload}mbps rtt: {rtt}ms, loss: {loss}%")

            for download, rtt, loss in self._cursor.execute("""SELECT DISTINCT download, rtt, loss
                                                               FROM basic""").fetchall():
                res = {}
                for upload, data in self._cursor.execute(f"""SELECT upload, data FROM basic
                                                             WHERE download={download}
                                                                   AND rtt={rtt}
                                                                   AND loss={loss}""").fetchall():
                    data = yaml.load(data, Loader=yaml.Loader)
                    res[upload] = data
                self.subplot(res, label="Upload", unit="mbps",
                             condition=f"download: {download}mbps rtt: {rtt}ms, loss: {loss}%")
        res = {}
        for technology, quality, data in self._cursor.execute("""SELECT technology, quality, data
                                                                 FROM errant""").fetchall():
            data = yaml.load(data, Loader=yaml.Loader)
            res[Connectivity(technology, quality)] = data
        self.subplot(res, label="Network")

    def subplot(self, data: Dict, label: str, unit: str = "", condition: str = ""):
        """
        Create the graphs for one set of experiment

        :param      data:       The data
        :type       data:       Dict
        :param      label:      The label
        :type       label:      str
        :param      unit:       The unit
        :type       unit:       str
        :param      condition:  The condition
        :type       condition:  str
        """
        if len(data) < 2:
            return
        condition = f" with {condition}" if condition != "" else ""
        unit = f" ({unit})" if unit != "" else ""
        self.subsubplot(data, labels=(f"{label}{unit}", "PLT (ms)"),
                        name=f"{label}/Page Load Time depending on {label}{condition}",
                        convert=lambda x : x["browsertime"].get_page_load_time())
        self.subsubplot(data, labels=(f"{label}{unit}", "SI (ms)"),
                        name=f"{label}/Speed Index depending on {label}{condition}",
                        convert=lambda x : x["browsertime"].get_speed_index())
        self.subsubplot(data, labels=(f"{label}{unit}", "ping (ms)"),
                        name=f"{label}/ping depending on {label}{condition}",
                        convert=lambda x : x["speedtest"].get_ping())
        self.subsubplot(data, labels=(f"{label}{unit}", "upload (mbps)"),
                        name=f"{label}/upload speed depending on {label}{condition}",
                        convert=lambda x : x["speedtest"].get_upload())
        self.subsubplot(data, labels=(f"{label}{unit}", "download (mbps)"),
                        name=f"{label}/download speed depending on {label}{condition}",
                        convert=lambda x : x["speedtest"].get_download())
        self.subsubplot(data, labels=(f"{label}{unit}", "download (mbps)"),
                        name=f"{label}/bulk download speed depending on {label}{condition}",
                        convert=lambda x : x["bulkTest"].get_download())

    def subsubplot(self, data: Dict, labels: Tuple[str, str], name: str, convert):
        """
        Create the graph for one metric

        :param      data:     The data
        :type       data:     Dict
        :param      labels:   The labels
        :type       labels:   str
        :param      name:     The name
        :type       name:     str
        :param      convert:  The convert
        :type       convert:  Dict -> List
        """
        res=[]
        index=[]
        for key, test in data.items():
            res.append(convert(test))
            index.append(key)
        res = pd.DataFrame(res, index=index, columns=["native", "masquerade", "squid"]).sort_index()
        try:
            fastplot.plot(data=res, path=f"/results/{name}", mode="boxplot_multi",
                          xlabel=labels[0], ylabel=labels[1],
                          legend=True, legend_ncol=3, figsize=(8, 4))
        except ValueError:
            print(f"Issue while creating {name}")
