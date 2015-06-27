from pizza.objects.vendor import Vendor
import selenium.webdriver.support.ui as ui

class Dominos(Vendor):

    toppings = {
        "Smoked Bacon Rashers": "bacon",
        "Baby Spinach": "spinach"
    }

    def _login(self):
        self.web_driver.get("https://www.dominos.co.uk")
        self.web_driver.find_element_by_id("txtPostcode").send_keys("sw116ru")
        self.web_driver.find_element_by_id("btnStoreSearch").click()
        self._wait_for_css(".btn.btn-neutral.btn-large")
        self.web_driver.find_element_by_css_selector(".btn.btn-neutral.btn-large").click()

    def _get_pizza_links(self):
        self._wait_for_cl("pizza")
        links = []
        for pizza in self.web_driver.find_element_by_id("Speciality Pizzas").find_elements_by_class_name("pizza"):
            footer = pizza.find_elements_by_class_name("section-footer")[0]
            order_button = footer.find_elements_by_class_name("order")[0].find_element_by_tag_name("a")
            links.append(order_button.get_attribute("href"))
        return links

    def _wait_for_cl(self, class_name):
        ui.WebDriverWait(self.web_driver, 10).until(
            lambda driver: len(self.web_driver.find_elements_by_class_name(class_name)) > 0
        )

    def _wait_for_id(self, id_name):
        ui.WebDriverWait(self.web_driver, 10).until(
            lambda driver: self.web_driver.find_element_by_id(id_name).is_displayed()
        )

    def _wait_for_css(self, css):
        ui.WebDriverWait(self.web_driver, 10).until(
            lambda driver: self.web_driver.find_element_by_css_selector(css).is_displayed()
        )

    def _parse_pizza_group(self, link):
        self.web_driver.get(link)
        self._wait_for_css(".pizza-name > h1")
        print self.web_driver.find_element_by_css_selector(".selected-toppings p").text
        print self.web_driver.find_element_by_css_selector(".pizza-name > h1").text
        print self.web_driver.find_element_by_css_selector(".pizza-price > h2").text

    def get_pizzas(self):
        self._login()
        for link in self._get_pizza_links():
            self._parse_pizza_group(link)
            break

        return [
            self._new_pizza("Mighty Meaty", ["pepperoni", "ham"], "large", 16, 12.5, "thin", 12),
            self._new_pizza("Hawaiian", ["pepperoni", "ham"], "large", 16, 12.5, "thin", 12),
        ]

    def get_meals(self):
        return []

    def get_sides(self):
        return []

    def get_desserts(self):
        return []