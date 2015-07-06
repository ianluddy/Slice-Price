from time import sleep
from slice_scanner.objects.vendor import Vendor

class Dominos(Vendor):

    id = "dominos"
    name = "Dominos Pizza"
    site = "https://www.dominos.co.uk/"

    diameter_reference = {
        "large": 13.5,
        "medium": 11.5,
        "small": 9.5,
        "personal": 7
    }

    slice_reference = {
        "large": 10,
        "medium": 8,
        "small": 6,
        "personal": 4
    }

    def _get_meals(self):
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

    #### Sides ####

    def _get_sides(self):
        self.web_driver.get("https://www.dominos.co.uk/menu")
        self._wait_for_alert(timeout=1)

        while not self._sides_ready():
            sleep(0.3)

        for side_id in self._get_side_ids():
            name = self._get_side_name(side_id)
            description = self._get_side_description(side_id)
            size = "standard"
            self._select_side(side_id)
            self._wait_for_js()
            while self._side_variants_remaining(side_id):
                quantity = self._get_side_variant_quantity(side_id)
                price = self._get_side_variant_price(side_id)
                self._new_side(
                    name, price, size, quantity, description
                )
                self._mark_side_variant_parsed(side_id)

    def _sides_ready(self):
        return int(self._script('return $("#Sides .product").length')) > 0

    def _get_side_name(self, side_id):
        return self._get_css_str("#Sides #%s h1:first" % str(side_id))

    def _side_variants_remaining(self, side_id):
        return self._script('return $("#%s .product-variants > .variant").length' % str(side_id)) > 0

    def _get_side_variant_quantity(self, side_id):
        quantity = self._get_str_int(self._get_side_variant_description(side_id))
        if quantity:
            return quantity
        return 1

    def _get_side_variant_description(self, side_id):
        return self._get_css_str('#%s .product-variants > .variant:first h1' % str(side_id))

    def _get_side_variant_price(self, side_id):
        return self._get_str_fl(
            self._get_css_str('#%s .product-variants > .variant:first h2' % str(side_id) )
        )

    def _mark_side_variant_parsed(self, side_id):
        self._script('$("#%s .product-variants > .variant").first().removeClass("variant").hide()' % str(side_id))

    def _get_side_description(self, side_id):
        return self._get_css_str("#Sides #%s p:first" % str(side_id))

    def _select_side(self, side_id):
        self._script('$("#%s .btn-positive[resource-name=Choose]").click()' % str(side_id))

    def _get_side_ids(self):
        return list(set(self._script('return $("#Sides .product").map(function(){ return parseInt($(this).attr("id"));}).get();')))

    #### Pizzas ####

    def _get_pizzas(self):
        for link in self._get_pizza_links():
            self._parse_pizza_group(link)

    def _get_pizza_links(self):
        self._wait_for_cl("pizza")
        self._wait_for_js()

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
            self._wait_for_alert(timeout=0.5)
            self._wait_for_alert_to_clear(timeout=0.5)
            self._wait_for_css(".pizza-name > h1")

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

        def _get_selected_price():
            return self._get_str_fl(self._get_css_str('.pizza-price > h2'))

        def _get_selected_title():
            return self._get_css_str('.pizza-name > h1')

        def _get_selected_toppings():
            return [t.strip() for t in self._get_css_str('.selected-toppings p').split(",")]

        def _crusts_remaining():
            return int(self._script('return $("button.crust-type").length')) > 0

        def _select_crust():
            return self._script(
                '$(".crust-item").first().find("button.crust-type").click(); $(".crust-item").first().remove();'
            )

        def _get_selected_crust():
            return self._get_css_str('button.crust-type:first')

        def _get_pizzas_per_size(size_txt):
            _get_size_btn(size_txt).click()
            self._acknowledge_dialog("selected crust is not available", True)
            size = size_txt.split(" ")[0]
            _open_crust_panel()
            self._wait_for_js()
            while _crusts_remaining():
                crust = _get_selected_crust()
                _select_crust()
                self._wait_for_js()
                self._new_pizza(
                    title,
                    toppings,
                    size,
                    self._diameter_from_size(size),
                    _get_selected_price(),
                    crust,
                    self._slices_from_size(size)
                )

        _wait_for_load()
        title = _get_selected_title()
        toppings = _get_selected_toppings()
        for size in _get_sizes():
            _get_pizzas_per_size(size)
