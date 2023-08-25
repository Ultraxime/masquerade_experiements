# -*- coding: utf-8 -*-
# @Author: Ultraxime
# @Last Modified by:   Ultraxime
# @Last Modified time: 2023-08-24 11:06:37
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
Module for the speed test result
"""
from typing import Dict
from typing import List

from result import Result


class SpeedTest(Result):
    """
    This class describes a speed test's result.
    """
    def __init__(self, folder: str = ".", name: str = "speedtest", **kwargs):
        super().__init__(folder, name, **kwargs)

    def plot(self):
        self.subplot("ping", "ms", lambda x : [int(x["ping_ms"])])
        self.subplot("download", "mbps", lambda x : [float(x["download_mbps"])])
        self.subplot("upload", "mbps", lambda x : [float(x["upload_mbps"])])

    def get_ping(self) -> Dict[str, List[int]]:
        """
        Gets the ping.

        :returns:   The ping.
        :rtype:     str * (int List) dict
        """
        return {"native": [int(test["ping_ms"]) for test in self._native],
                "masquerade" : [int(test["ping_ms"]) for test in self._masquerade],
                "squid": [int(test["ping_ms"]) for test in self._squid]}

    def get_download(self) -> Dict[str, List[float]]:
        """
        Gets the download.

        :returns:   The download speed.
        :rtype:     str * (float List) dict
        """
        return {"native": [float(test["download_mbps"]) for test in self._native],
                "masquerade" : [float(test["download_mbps"]) for test in self._masquerade],
                "squid": [float(test["download_mbps"]) for test in self._squid]}

    def get_upload(self) -> Dict[str, List[float]]:
        """
        Gets the upload.

        :returns:   The upload speed.
        :rtype:     str * (float List) dict
        """
        return {"native": [float(test["upload_mbps"]) for test in self._native],
                "masquerade" : [float(test["upload_mbps"]) for test in self._masquerade],
                "squid": [float(test["upload_mbps"]) for test in self._squid]}
