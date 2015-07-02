from time import sleep
from pizza.objects.vendor import Vendor

class Dominos(Vendor):

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

    def _acknowledge_dialog(self, containing_text, confirm):
        self._wait_for_css(".modal", timeout=0.5)
        for modal in self.web_driver.find_elements_by_class_name("modal"):
            if modal.is_displayed():
                if containing_text in modal.text.encode("utf-8").lower():
                    if confirm:
                        modal.find_elements_by_class_name("btn-positive")[0].click()
                    else:
                        modal.find_elements_by_class_name("btn-negative")[0].click()
                    self._wait_for_css_to_clear(".modal-backdrop.fade.in", timeout=2)

    #### Pizzas ####

    def _get_pizzas(self):
        for link in self._get_pizza_links():
            self._parse_pizza_group(link)

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

        def _wait_for_load():
            self.web_driver.get(link)
            self._wait_for_alert()
            self._wait_for_alert_to_clear()
            self._wait_for_css(".pizza-name > h1")

        def _get_group_info():
            title = self._get_css_txt(".pizza-name > h1").lower()
            toppings = [t.strip().lower() for t in self._get_css_txt(".selected-toppings p").split(",")]
            return title, toppings

        def _open_size_panel():
            self._wait_for_id("size")
            if self._get_css("#size.selected"):
                return None
            self.web_driver.find_element_by_id("size").click()
            self._wait_for_cl("pizza-size")

        def _open_crust_panel():
            self._wait_for_id("crust")
            if self._get_css("#crust.selected"):
                return None
            self.web_driver.find_element_by_id("crust").click()
            self._wait_for_cl("crust-type")

        def _get_size_elements():
            _open_size_panel()
            return self.web_driver.find_elements_by_class_name("pizza-size")

        def _get_sizes():
            return [btn.text.encode("utf-8").lower() for btn in _get_size_elements()]

        def _get_size_btn(size):
            for btn in _get_size_elements():
                if btn.text.encode("utf-8").lower() == size:
                    return btn

        def _get_crust_elements():
            _open_crust_panel()
            return self.web_driver.find_elements_by_class_name("crust-type")

        def _snapshot_selection(crust):
            size = self._get_css_txt("#size-selector > .selection > span").split(" ")[0].lower()
            price = self._get_str_fl(self._get_css_txt(".pizza-price > h2"))
            self._new_pizza(title, toppings, size, self._diameter_from_size(size), price, crust,
                            self._slices_from_size(size))

        def _get_pizzas_per_size(size_txt):
            _get_size_btn(size_txt).click()
            self._acknowledge_dialog("selected crust is not available", True)
            for crust_btn in _get_crust_elements():
                try:
                    sleep(0.5)
                    crust_btn.click()
                    crust_btn.click() # hmmm
                    sleep(0.5)
                    _snapshot_selection(crust_btn.text.encode("utf-8").lower())
                except Exception, e:
                    print str(e)
                    print "crust fail"

        _wait_for_load()
        title, toppings = _get_group_info()
        for size in _get_sizes():
            _get_pizzas_per_size(size)
