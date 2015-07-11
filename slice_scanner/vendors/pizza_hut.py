from slice_scanner.objects.vendor import Vendor


class PizzaHut(Vendor):

    id = "pizza_hut"
    name = "Pizza Hut"
    site = "https://www.pizzahut.co.uk/"

    diameter_reference = {
        "large": 14,
        "medium": 12,
        "small": 9.5,
    }

    slice_reference = {
        "large": 10,
        "medium": 8,
        "small": 6
    }

    def _get_meals(self):
        return []

    def _get_desserts(self):
        return []

    def _get_sides(self):
        return []

    def _get_pizzas(self):

        def _get_pizza_count():
            return self._script('return $(".pizza-product").length')

        def _get_pizza_title(index):
            return self._script('return $($(".pizza-product").get(%s)).find("h3").text()' % index).strip()

        def _get_pizza_description(index):
            return self._script('return $($(".pizza-product").get(%s)).find("p").text()' % index).strip()

        def _mark_pizza_sizes_for_parsing():
            return self._script('$(".pizzasize li").each(function(){ $(this).addClass("unparsed")})')

        def _mark_pizza_bases_for_parsing():
            return self._script('$(".pizzabase li").each(function(){ $(this).addClass("unparsed")})')

        def _select_next_pizza_base(index):
            return self._script(
                'return $($(".pizza-product").get(%s)).find(".pizzabase li.unparsed:first").removeClass("unparsed").find("a").click().text()' %
                index
            )

        def _select_next_pizza_size(index):
            return self._script(
                'return $($(".pizza-product").get(%s)).find(".pizzasize li.unparsed:first").removeClass("unparsed").find("a").click().text()' %
                index
            ).lower()

        def _get_pizza_price(index):
            return self._script('return $($(".pizza-product").get(%s)).find(".pizza-price span:last").text()' % index).strip()

        self._wait_for_css(".pizza-product")
        self._wait_for_css(".pizzabase li")

        _mark_pizza_bases_for_parsing()

        for i in range(_get_pizza_count()):
            i += 5
            title = _get_pizza_title(i)
            toppings = [t.strip() for t in _get_pizza_description(i).split(",")]

            while True:
                base = _select_next_pizza_base(i)
                self._wait_for_js()
                if base:
                    _mark_pizza_sizes_for_parsing()
                    while True:
                        size = _select_next_pizza_size(i)
                        self._wait_for_js()
                        price = self._get_str_fl(_get_pizza_price(i))
                        if size:
                            self._new_pizza(title, toppings, size, price, base)
                        else:
                            break
                else:
                    break

    def _login(self):
        self.web_driver.get("https://www.pizzahut.co.uk/menu/pizza")

        self._wait_for_css(".btn-order")
        self._script('$(".btn-order:first").click()')

        self._wait_for_id("optCollection")
        self._wait_for_js()
        self._get_id("optCollection").click()
        self._get_id("ajax-postcode-txt").send_keys("sw185lt")
        self._get_id("get-store-btn").click()

        self._wait_for_css('.store-start-order a:first')
        self._script('$(".store-start-order a:first").click()')
