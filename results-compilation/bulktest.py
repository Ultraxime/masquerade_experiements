from result import Result


class BulkTest(Result):
    def __init__(self, folder: str = ".", name: str = "bulk_download"):
        super().__init__(folder, name)
    
    def plot(self):
        self.subplot("bulk download", unit="mbps", convert=lambda x : [int(x) / 1000000], scale="log")
    