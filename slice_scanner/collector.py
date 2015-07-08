import logging
from crontab import CronTab
import time
from vendors import dominos, pizza_hut
from selenium import webdriver

class Collector(object):

    def __init__(self, frequency, queue):
        self.cron = CronTab(frequency)
        self.vendors = [
            dominos.Dominos(queue),
            pizza_hut.PizzaHut(queue),
        ]

    def _start_webdriver(self):
        return webdriver.Chrome('C:\\chromeDRIVER.exe', service_args=['--ignore-ssl-errors=true'])
        # return self.web_driver = webdriver.PhantomJS('C:\\phantomjs.exe', service_args=['--ignore-ssl-errors=true'])
        # return webdriver.Firefox()

    def _collect(self):
        web_driver = self._start_webdriver()
        for session in self.vendors:
            session.set_driver(web_driver)
            session.parse()
        web_driver.quit()

    def vendor_info(self):
        vendor_info = {}
        for vendor in self.vendors:
            vendor_dict = vendor.to_dict()
            vendor_info[vendor_dict["id"]] = vendor_dict
        return vendor_info

    def run(self):
        logging.info("Collector Running")
        while True:
            time.sleep(self.cron.next())
            self._collect()
