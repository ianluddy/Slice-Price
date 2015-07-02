import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import re
import abc

class Parser(object):
    __metaclass__ = abc.ABCMeta
    web_driver = None

    def set_driver(self, web_driver):
        self.web_driver = web_driver

    #### Implement ####

    @abc.abstractmethod
    def parse(self):
        """ Get list of Pizzas """

    #### DOM ####

    def _get_css(self, selector):
        try:
            return self.web_driver.find_element_by_css_selector(selector)
        except NoSuchElementException:
            return None

    def _get_id(self, selector):
        try:
            return self.web_driver.find_element_by_id(selector)
        except NoSuchElementException:
            return None

    def _get_class(self, selector):
        try:
            return self.web_driver.find_elements_by_class_name(selector)[0]
        except NoSuchElementException:
            return None

    def _wait_for_cl(self, selector, timeout=3):
        try:
            ui.WebDriverWait(self.web_driver, timeout).until(
                lambda driver: len(self.web_driver.find_elements_by_class_name(selector)) > 0
            )
        except TimeoutException:
            pass

    def _wait_for_id(self, selector, timeout=3):
        try:
            ui.WebDriverWait(self.web_driver, timeout).until(
                lambda driver: self.web_driver.find_element_by_id(selector).is_displayed()
            )
        except TimeoutException:
            pass

    def _wait_for_css(self, selector, timeout=3):
        try:
            ui.WebDriverWait(self.web_driver, timeout).until(
                lambda driver: self.web_driver.find_element_by_css_selector(selector).is_displayed()
            )
        except TimeoutException:
            pass

    def _wait_for_css_to_clear(self, selector, timeout=3):
        try:
            ui.WebDriverWait(self.web_driver, timeout).until(
                lambda driver: not self.web_driver.find_element_by_css_selector(selector).is_displayed()
            )
        except TimeoutException:
            pass

    def _wait_for_alert(self, timeout=2):
        try:
            ui.WebDriverWait(self.web_driver, timeout).until(EC.alert_is_present())
            self.web_driver.switch_to.alert.accept()
        except TimeoutException:
            return

    def _wait_for_alert_to_clear(self, timeout=2):
        try:
            ui.WebDriverWait(self.web_driver, timeout).until(
                lambda alert: not EC.alert_is_present()
            )
        except TimeoutException:
            return

    def _get_css_txt(self, selector):
        return self.web_driver.find_element_by_css_selector(selector).text.encode("utf-8")

    def _get_id_txt(self, selector):
        return self.web_driver.find_element_by_id(selector).text.encode("utf-8")

    #### STRING ####

    def _get_str_int(self, string):
        return int(re.search(r'\d+', string).group())

    def _get_str_fl(self, string):
        return float(re.findall("\d+.\d+", string)[0])