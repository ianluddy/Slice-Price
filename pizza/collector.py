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
            self.queue.put(self._get_vendor_data(vendor))

    def _get_vendor_data(self, vendor):
        return {
            "vendor": vendor.id,
            "pizza": vendor.get_pizzas(),
            "meals": vendor.get_meals(),
            "sides": vendor.get_sides(),
            "desserts": vendor.get_desserts()
        }

    def run(self):
        logging.info("Collector Running")
        while True:
            self._collect()
            time.sleep(self.cron.next())