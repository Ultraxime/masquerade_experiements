import pandas as pd
import os
import yaml
import time
import sqlite3

import fastplot

# If up and download are correlated
BANDWIDTH = True

class FullResults:
    def __init__(self, folder: str = "."):
        self._connection = sqlite3.connect("%s/full_results %s.db" % (folder, time.asctime()))
        
        self._cursor = self._connection.cursor()
        self._cursor.execute("CREATE TABLE basic(upload, download, rtt, loss, data)")
        self._cursor.execute("CREATE TABLE errant(technology, quality, operator, country, data)")
        
        tests = [test for test in os.scandir(folder)]
        tests.sort(key=lambda f: f.path)

        for test in tests:
            if ".yml" in test.name:
                try:
                    self._add_basic(test)
                except ValueError:
                    try:
                        self._add_errant(test)
                    except:
                        print(test.name)
        
    def _add_basic(self, test):
        data = test.name.split(" ")
        upload = int(data[0])
        download = int(data[1])
        rtt = int(data[2])
        loss = int(data[3])
        with open(test.path, 'r', encoding='utf-8') as file:
            data = file.read()
            if self._cursor.execute(f"SELECT * FROM basic WHERE upload={upload} AND download={download} AND rtt={rtt} AND loss={loss}").fetchall() != []:
                self._cursor.execute(f"UPDATE basic SET data={data} WHERE upload={upload} AND download={download} AND rtt={rtt} AND loss={loss}")
            else:
                self._cursor.execute(f"INSERT INTO basic VALUES ({upload}, {download}, {rtt}, {loss}, \"{data}\")")
            self._connection.commit()

    def _add_errant(self, test):
        data = test.name.split(" ")
        technology = data[0]
        quality = data[1]
        operator = data[2]
        country = data[3]
        with open(test.path, 'r', encoding='utf-8') as file:
            data = file.read()
            request = f"INSERT INTO errant VALUES ({technology}, {quality}, {operator}, {country}, \"{data}\")"
            self._cursor.execute(request)
            self._connection.commit()

    def plot(self):
        for upload, download, rtt in self._cursor.execute("SELECT DISTINCT upload, download, rtt from basic").fetchall():
            res = {}
            for loss, data in self._cursor.execute(f"SELECT loss, data FROM basic WHERE upload={upload} AND download={download} AND rtt={rtt}").fetchall():
                data = yaml.load(data, Loader=yaml.Loader)
                res[loss] = data
            self.subplot(res, label="Loss", unit="%", condition=f"upload: {upload}mbps download: {download}mbps, rtt: {rtt}ms")
        for upload, download, loss in self._cursor.execute("SELECT DISTINCT upload, download, loss from basic").fetchall():
            res = {}
            for rtt, data in self._cursor.execute(f"SELECT rtt, data FROM basic WHERE upload={upload} AND download={download} AND loss={loss}").fetchall():
                data = yaml.load(data, Loader=yaml.Loader)
                res[rtt] = data
            self.subplot(res, label="RTT", unit="ms", condition=f"upload: {upload}mbps download: {download}mbps, loss: {loss}%")
        
        if BANDWIDTH:
            for rtt, loss in self._cursor.execute("SELECT DISTINCT rtt, loss from basic").fetchall():
                res = {}
                for upload, data in self._cursor.execute(f"SELECT upload, data FROM basic WHERE rtt={rtt} AND loss={loss}").fetchall():
                    data = yaml.load(data, Loader=yaml.Loader)
                    res[upload] = data
                self.subplot(res, label="Upload", unit="mbps", condition=f"rtt: {rtt}ms, loss: {loss}%")
        else:
            for upload, rtt, loss in self._cursor.execute("SELECT DISTINCT upload, rtt, loss from basic").fetchall():
                res = {}
                for download, data in self._cursor.execute(f"SELECT download, data FROM basic WHERE upload={upload} AND rtt={rtt} AND loss={loss}").fetchall():
                    data = yaml.load(data, Loader=yaml.Loader)
                    res[download] = data
                self.subplot(res, label="Download", unit="mbps", condition=f"upload: {upload}mbps rtt: {rtt}ms, loss: {loss}%")
            
            for download, rtt, loss in self._cursor.execute("SELECT DISTINCT download, rtt, loss from basic").fetchall():
                res = {}
                for upload, data in self._cursor.execute(f"SELECT upload, data FROM basic WHERE download={download} AND rtt={rtt} AND loss={loss}").fetchall():
                    data = yaml.load(data, Loader=yaml.Loader)
                    res[upload] = data
                self.subplot(res, label="Upload", unit="mbps", condition=f"download: {download}mbps rtt: {rtt}ms, loss: {loss}%")

    def subplot(self, data, label, unit, condition):
        def pageLoadTimeAcc(data):
            res = {"native": [],
                   "masquerade" : [],
                   "squid": []}
            data = data["browsertime"]
            for website in data._native:
                if (website in data._masquerade and website in data._squid
                    and len(data._native[website].pageLoadTime) == len(data._masquerade[website].pageLoadTime)
                    and len(data._native[website].pageLoadTime) == len(data._squid[website].pageLoadTime)):
                    
                    res["native"].extend(data._native[website].pageLoadTime)
                    res["masquerade"].extend(data._masquerade[website].pageLoadTime)
                    res["squid"].extend(data._squid[website].pageLoadTime)
            return res

        def speedIndexAcc(data):
            res = {"native": [],
                   "masquerade" : [],
                   "squid": []}
            data = data["browsertime"]
            for website in data._native:
                if (website in data._masquerade and website in data._squid
                    and len(data._native[website].speedIndex) == len(data._masquerade[website].speedIndex)
                    and len(data._native[website].speedIndex) == len(data._squid[website].speedIndex)):
                    
                    res["native"].extend(data._native[website].speedIndex)
                    res["masquerade"].extend(data._masquerade[website].speedIndex)
                    res["squid"].extend(data._squid[website].speedIndex)
            return res
            
        self.subsubplot(data, labels=(f"{label} ({unit})", "PLT (ms)"), name=f"{label}/Page Load Time depending on {label} with {condition}", convert=lambda x : pageLoadTimeAcc(x))
        self.subsubplot(data, labels=(f"{label} ({unit})", "SI (ms)"), name=f"{label}/Speed Index depending on {label} with {condition}", convert=lambda x : speedIndexAcc(x))

    def subsubplot(self, data, labels, name, convert):
        res=[]
        index=[]
        for key, test in data.items():
            res.append(convert(test))
            index.append(key)
        print(res)
        res = pd.DataFrame(res, index=index, columns=["native", "masquerade", "squid"])
        print(res)
        fastplot.plot(data=res, path="/results/%s" % name, mode="boxplot_multi", xlabel=labels[0], ylabel=labels[1], legend=True, legend_ncol=3, figsize=(8,4   ))