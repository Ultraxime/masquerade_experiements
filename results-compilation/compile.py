from browsertime import BrowserTime
from speedtest import SpeedTest
from bulktest import BulkTest


browsertime = BrowserTime("/results")
browsertime.save()
browsertime.plot()

SpeedTest("/results").plot()
BulkTest("/results").plot()

