# -*- coding: utf-8 -*-
# @Author: Ultraxime
# @Last Modified by:   Ultraxime
# @Last Modified time: 2023-08-24 11:11:06
#
# This file is part of Masquerade experiements.
#
# Masquerade experiements is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or any later version.
#
# Masquerade experiements is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Masquerade experiements. If not, see <https://www.gnu.org/licenses/>.
"""
Base class for the results
"""
import os
import time
from typing import Iterable
from typing import List
from typing import Optional

import matplotlib.pyplot as plt
import yaml


class Result:
    """
    This class describes the result of an experiment
    """
    _native: List
    _masquerade: List
    _squid: List

    def __init__(self, folder: str = ".", name: str = "",
                 _native: Optional[List] = None,
                 _masquerade: Optional[List] = None,
                 _squid: Optional[List] = None):
        if _native is not None and _masquerade is not None and _squid is not None:
            self._native = _native
            self._masquerade = _masquerade
            self._squid = _squid
            return

        content = None
        for file in os.scandir(folder):
            if not file.is_dir() and name in file.name:
                with open(file.path, "r", encoding="utf-8") as file:
                    content = yaml.safe_load(file)

        if content is None:
            self._masquerade = []
            self._squid = []
            self._native = []
            return

        try:
            self._masquerade = content["proxy-masquerade"]
        except KeyError:
            self._masquerade = []
        try:
            self._squid = content["proxy-squid"]
        except KeyError:
            self._squid = []
        try:
            self._native = content["native"]
        except KeyError:
            self._native = []

    def develop(self, field: Iterable, convert) -> List:
        """
        Convert a set of test's results in one sorted list

        :param      field:    The field
        :type       field:    Iterable
        :param      convert:  The convert
        :type       convert:  Any -> List

        :returns:   the sorted list
        :rtype:     List
        """
        res = []
        for test in field:
            res.extend(convert(test))
        res.sort()
        return res


    def subplot(self, name: str, unit: str = "",
                convert = lambda x: [float(x)], scale: str = "linear"):
        """
        Create a subplot of the result

        :param      name:     The name
        :type       name:     str
        :param      unit:     The unit
        :type       unit:     str
        :param      convert:  The convert
        :type       convert:  Any -> List
        :param      scale:    The scale
        :type       scale:    str
        """
        mini = None
        maxi = None

        masquerade = self.develop(self._masquerade, convert)
        if masquerade:
            plt.plot(masquerade,
                     [(i+1)/len(masquerade) for i in range(len(masquerade))],
                     label=f"masquerade ({len(masquerade)} tests)")
            mini = masquerade[0]
            maxi = masquerade[-1]

        squid = self.develop(self._squid, convert)
        if squid:
            plt.plot(squid,
                     [(i+1)/len(squid) for i in range(len(squid))],
                     label=f"squid ({len(squid)} tests)")
            if mini and maxi:
                mini = min(mini, squid[0])
                maxi = max(maxi, squid[-1])
            else:
                mini = squid[0]
                maxi = squid[-1]

        native = self.develop(self._native, convert)
        if native:
            plt.plot(native,
                     [(i+1)/len(native) for i in range(len(native))],
                     label=f"native ({len(native)} tests)")
            if mini and maxi:
                mini = min(mini, native[0])
                maxi = max(maxi, native[-1])
            else:
                mini = native[0]
                maxi = native[-1]

        plt.axis([mini, maxi, 0, 1])
        plt.ylabel('ECDF')
        plt.xlabel(f'{name}' + (f" ({unit})" if unit != "" else ""))
        plt.xscale(scale)

        plt.legend(loc="lower right")

        plt.savefig(f'/results/results/{name} {time.asctime()}.png')
        plt.clf()

    def plot(self):
        """
        Create all the plot for the result
        """
        self.subplot(type(self).__name__)

    def get_field(self, field: str) -> List:
        """
        Gets the field.

        :param      field:  The field
        :type       field:  str

        :returns:   The field.
        :rtype:     List
        """
        match field:
            case "native":
                return self._native
            case "masquerade":
                return self._masquerade
            case "squid":
                return self._squid
            case _:
                raise ValueError
