import pandas as pd
import os
import yaml
import time

import fastplot


class FullResults:
	def __init__(self, folder: str = "."):
	    self._basic = {}
	    self._errant = {}

	    tests = [test for test in os.scandir(folder)]
	    tests.sort(key=lambda f: f.path)

	    for test in tests:
	    	try:
	    		self._add_basic(test)
	    	except ValueError:
	    		self._add_errant(test)
	    
	def _add_basic(self, test):
		data = test.name.split(" ")
		upload = int(data[0])
		download = int(data[1])
		rtt = int(data[2])
		loss = int(data[3])
		with open(test.path, 'r', encoding='utf-8') as file:
			if loss not in self._basic:
				self._basic[loss] = {}
			if upload not in self._basic[loss]:
				self._basic[loss][upload] = {}
			if download not in self._basic[loss][upload]:
				self._basic[loss][upload][download] = {}
			self._basic[loss][upload][download][rtt] = yaml.load(file, Loader=yaml.Loader)

	def _add_errant(self, test):
		data = test.name.split(" ")
		with open(test.path, 'r', encoding='utf-8') as file:
			self._errant[data[0]][data[1]][data[2]][data[3]] = yaml.load(file, Loader=yaml.Loader)

	def save(self):
		with open("results/full_results %s" % time.asctime(), 'w', encoding='utf-8') as file:
			yaml.dump(self, file)

	def plot(self):
		for loss, data in self._basic.items():
			for upload, data2 in data.items():
				for download, data3 in data2.items():
					self.subplot(data3)
					

	def subplot(self, data, convert = lambda x : x):
		def pageLoadTimeAcc(data):
			res = {"native": [],
				   "masquerade" : [],
				   "squid": []}
			for website, value in data["browsertime"]._native:
				res["native"].extend(value.pageLoadTime)
			for website, value in data["browsertime"]._masquerade:
				res["masquerade"].extend(value.pageLoadTime)
			for website, value in data["browsertime"]._squid:
				res["squid"].extend(value.pageLoadTime)
			return res

		self.subsubplot(data, lambda x : pageLoadTimeAcc(convert(x)))

	def subsubplot(self, data, convert):
		res={}
		for label, test in data.items():
			res[str(label)] = convert(test)
		res = pd.DataFrame.from_dict(res)
		# print(res)
		fastplot.plot(data=res, path="/results/test.png", mode="boxplot_multi")