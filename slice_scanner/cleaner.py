import logging
from crontab import CronTab
import time

class Cleaner(object):

    def __init__(self, frequency, data_validity_hours, db_wrapper):
        self.cron = CronTab(frequency)
        self.data_validity = data_validity_hours
        self.db = db_wrapper

    def run(self):
        logging.info("Cleaner Running")
        while True:
            time.sleep(self.cron.next())
            self._remove_stale_data()

    def _remove_stale_data(self):
        stale_data_cutoff = time.time() - (self.data_validity * 60 * 60)
        self.db.remove("pizza", {"stamp": {"$lt": stale_data_cutoff}})
        self.db.remove("sides", {"stamp": {"$lt": stale_data_cutoff}})
