import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium import webdriver

class Parser():

    web_driver = webdriver.Chrome('C:\\chromeDRIVER.exe', service_args=['--ignore-ssl-errors=true'])
    # web_driver = webdriver.PhantomJS('C:\\phantomjs.exe', service_args=['--ignore-ssl-errors=true'])

    #### DOM ####

    def _wait_for_cl(self, selector):
        ui.WebDriverWait(self.web_driver, 10).until(
            lambda driver: len(self.web_driver.find_elements_by_class_name(selector)) > 0
        )

    def _wait_for_id(self, selector):
        ui.WebDriverWait(self.web_driver, 10).until(
            lambda driver: self.web_driver.find_element_by_id(selector).is_displayed()
        )

    def _wait_for_css(self, selector):
        ui.WebDriverWait(self.web_driver, 10).until(
            lambda driver: self.web_driver.find_element_by_css_selector(selector).is_displayed()
        )

    def _get_css_txt(self, selector):
        return self.web_driver.find_element_by_css_selector(selector).text.encode("utf-8")

    def _get_id_txt(self, selector):
        return self.web_driver.find_element_by_id(selector).text.encode("utf-8")

    def _wait_for_alert(self):
        try:
            ui.WebDriverWait(self.web_driver, 2).until(EC.alert_is_present())
            self.web_driver.switch_to.alert.accept()
        except TimeoutException:
            return

    #### STRING ####

    def _get_str_int(self, string):
        return int(re.search(r'\d+', string).group())

    def _get_str_fl(self, string):
        return float(re.findall("\d+.\d+", string)[0])