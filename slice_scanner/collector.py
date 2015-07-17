import logging
from crontab import CronTab
import time
from vendors import dominos, pizza_hut, pizza_express, papa_johns
from selenium import webdriver

class Collector(object):

    def __init__(self, frequency, web_driver, queue):
        self.cron = CronTab(frequency)
        self.web_driver = web_driver
        self.vendors = [
            dominos.Dominos(queue),
            papa_johns.PapaJohns(queue),
            pizza_hut.PizzaHut(queue),
            pizza_express.PizzaExpress(queue),
        ]

    def _start_webdriver(self):
        if "chrome" in self.web_driver.lower():
            return webdriver.Chrome(self.web_driver, service_args=['--ignore-ssl-errors=true'])
        if "fire" in self.web_driver.lower():
            return webdriver.Firefox()
        return webdriver.PhantomJS(self.web_driver)

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
            self._collect()
            time.sleep(self.cron.next())
