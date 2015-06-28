from pizza.objects.vendor import Vendor
from pizza.objects.parser import Parser
from time import sleep

class Dominos(Vendor, Parser):

    toppings = {
        "smoked bacon rashers": "bacon",
        "baby spinach": "spinach",
        "sunblush baby tomatoes": "tomatoes"
    }

    diameters = {
        "large": 13.5,
        "medium": 11.5,
        "small": 9.5,
        "personal": 7
    }

    slices = {
        "large": 10,
        "medium": 8,
        "small": 6,
        "personal": 4
    }

    def _get_meals(self):
        return []

    def _get_sides(self):
        return []

    def _get_desserts(self):
        return []

    def _login(self):
        self.web_driver.get("https://www.dominos.co.uk")
        self._wait_for_alert()
        self.web_driver.find_element_by_id("txtPostcode").send_keys("sw116ru")
        self.web_driver.find_element_by_id("btnStoreSearch").click()
        self._wait_for_css(".btn.btn-neutral.btn-large")
        self.web_driver.find_element_by_css_selector(".btn.btn-neutral.btn-large").click()

    #### Pizzas ####

    def _get_pizzas(self):
        self._login()
        pizzas = []
        for link in self._get_pizza_links():
            pizzas += self._parse_pizza_group(link)
        return pizzas

    def _get_pizza_links(self):
        self._wait_for_cl("pizza")

        def _get_links(section):
            links = []
            for pizza in self.web_driver.find_element_by_id(section).find_elements_by_class_name("pizza"):
                footer = pizza.find_elements_by_class_name("section-footer")[0]
                order_button = footer.find_elements_by_class_name("order")[0].find_element_by_tag_name("a")
                links.append(order_button.get_attribute("href"))
            return links

        return _get_links("Gourmet Pizzas") + _get_links("Speciality Pizzas")

    def _parse_pizza_group(self, link):
        # Wait
        self.web_driver.get(link)
        self._wait_for_alert()
        sleep(2)
        self._wait_for_css(".pizza-name > h1")

        # Get pizza group info
        title = self._get_css_txt(".pizza-name > h1").lower()
        toppings = [t.strip().lower() for t in self._get_css_txt(".selected-toppings p").split(",")]
        pizzas = []

        def _select_size(element):
            element.click()
            sleep(1)
            size = self._get_css_txt("#size-selector > .selection > span").split(" ")[0].lower()
            price = self._get_str_fl(self._get_css_txt(".pizza-price > h2"))
            return size, self._diameter_from_size(size), self._slices_from_size(size), price

        # Grab details for each size
        self.web_driver.find_element_by_id("size").click()
        self._wait_for_cl("pizza-size")
        for btn in self.web_driver.find_elements_by_class_name("pizza-size"):
            size, diameter, slices, price = _select_size(btn)
            pizzas.append(self._new_pizza(title, toppings, size, diameter, price, "classic", slices))

        return pizzas