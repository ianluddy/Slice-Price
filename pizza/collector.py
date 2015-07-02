import logging
from crontab import CronTab
import time
from vendors import dominos
from selenium import webdriver

class Collector(object):
    vendors = [
        dominos.Dominos()
    ]

    def __init__(self, frequency, queue):
        self.cron = CronTab(frequency)
        self.queue = queue
        self.web_driver = webdriver.Chrome('C:\\chromeDRIVER.exe', service_args=['--ignore-ssl-errors=true'])
        # self.web_driver = webdriver.PhantomJS('C:\\phantomjs.exe', service_args=['--ignore-ssl-errors=true'])
        # self.web_driver = webdriver.Firefox()

    def _collect(self):
        for session in self.vendors:
            session.set_driver(self.web_driver)
            self.queue.put(session.parse())
        self.web_driver.quit()

    def run(self):
        logging.info("Collector Running")
        while True:
            self._collect()
            time.sleep(self.cron.next())