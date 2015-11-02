import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re
import abc

class Parser(object):
    __metaclass__ = abc.ABCMeta
    web_driver = None
    page_wait = 0.4 # Wait time we use for animations, ajax loading etc

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

    def _wait(self):
        sleep(self.page_wait)

    def _script(self, script):
        return self.web_driver.execute_script(script)

    def _element_count(self, selector):
        return self._script('return $("%s").length' % selector)

    def _select_next_by_class(self, classname):
        return self._script("$('.%s:first').removeClass('%s').click()" % (classname, classname))

    def _wait_for_alert_to_clear(self, timeout=2):
        try:
            ui.WebDriverWait(self.web_driver, timeout).until(
                lambda alert: not EC.alert_is_present()
            )
        except TimeoutException:
            return

    def _get_css_str(self, selector):
        while True:
            string = self._script('return $("%s").text()' % selector).encode("utf-8")
            if string:
                return string
            sleep(0.2)

    def _get_id_txt(self, selector):
        return self.web_driver.find_element_by_id(selector).text.encode("utf-8")

    #### STRING ####

    @staticmethod
    def _get_str_int(string):
        try:
            return int(re.search(r'\d+', string).group())
        except AttributeError:
            return None

    @staticmethod
    def _get_str_fl(string):
        try:
            return float(re.findall("\d+.\d+", string)[0])
        except IndexError, AttributeError:
            return None

    @staticmethod
    def _strip_to_ascii(string):
        return ''.join([i if ord(i) < 128 else '' for i in string])

    @staticmethod
    def _normalise_parsed_data(kwargs):

        def _punify(data):
            return data.encode("punycode").split("-")[0]

        for key, value in kwargs.iteritems():
            if key not in ["img"]:
                if type(value) in [str, unicode]:
                    kwargs[key] = _punify(value)
                elif type(value) in [list]:
                    kwargs[key] = [_punify(item) for item in value]
        return kwargs
