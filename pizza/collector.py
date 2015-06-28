import logging
from crontab import CronTab
import time

class Collector():

    def __init__(self, vendors, frequency, queue):
        self.vendors = vendors
        self.cron = CronTab(frequency)
        self.queue = queue

    def _collect(self):
        for vendor in self.vendors:
            self.queue.put(vendor.get())

    def run(self):
        logging.info("Collector Running")
        while True:
            self._collect()
            time.sleep(self.cron.next())