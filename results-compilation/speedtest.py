from result import Result


class SpeedTest(Result):
    def __init__(self, folder: str = ".", name: str = "speedtest"):
        super().__init__(folder, name)
    
    def plot(self):
        self.subplot("ping", "ms", lambda x : [int(x["ping_ms"])])
        self.subplot("download", "mbps", lambda x : [float(x["download_mbps"])])
        self.subplot("upload", "mbps", lambda x : [float(x["upload_mbps"])])
    