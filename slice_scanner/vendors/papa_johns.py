# coding=utf-8
from slice_scanner.objects.vendor import Vendor

class PapaJohns(Vendor):

    id = "Papa Johns"
    site = "http://www.papajohns.ie"

    diameter_reference = {
        "small": 10,
        "medium": 12,
        "large": 14
    }

    slice_reference = {
        "small": 6,
        "medium": 8,
        "large": 10
    }

    def _login(self):
        self.web_driver.get("https://order.papajohns.ie/")
        self._wait_for_css("#countyList")
        self._script('$("#countyList ul ul a:first").click()')
        self._wait()
        self._script('$(".button.startOrder-link").click()')
        self._wait()
        self._wait()
        self._script('$("#orderSetupSteps input:first").click()')
        self._wait()
        self._script('$("#OrderSetupSubmit").click()')
        self._wait()

    def _get_sides(self):

        def _mark_sides_unparsed():
            return self._script('$(".row").addClass("unparsed")')

        def _mark_side_parsed():
            return self._script('$(".row.unparsed:first").removeClass("unparsed")')

        def _remaining_unparsed_sides():
            return self._element_count(".row.unparsed")

        def _get_name():
            return self._get_css_str(".row.unparsed:first .product-name").strip()

        def _get_image():
            return self._get_css_attr(".row.unparsed:first .product-image img", "src")

        def _get_price():
            return self._get_str_fl(self._get_css_str(".row.unparsed:first .product-price-value").strip())

        def _get_description():
            return self._get_css_str(".row.unparsed:first .product-desc-with-image")

        self._wait()
        self._script('$("a:visible:contains(\'%s\')").click()' % 'Sides')
        self._wait()
        self._wait()
        self._wait()
        _mark_sides_unparsed()
        self._wait()
        while _remaining_unparsed_sides() > 0:
            self._new_side(_get_name(), _get_price(), _get_image(), _get_description())
            self._wait()
            _mark_side_parsed()
            self._wait()

    def _get_pizzas(self):

        def _get_ids():
            links = []
            while self._element_count("input[name=MenuElementID]") > 0:
                links.append(_next_unparsed_pizza())
            return links

        def _next_unparsed_pizza():
            return self._script('return $("input[name=MenuElementID]:first").attr("name","").attr("value")')

        def _follow_pizza_link(pizza_id):
            self._wait()
            self._script('$("input[value=%s]").siblings(".productCustomizeButtons").find("a").click()' % pizza_id)
            self._wait()

        def _select_pizza_category(title):
            self._wait()
            self._script('$("a:contains(\'%s\')").click()' % title)
            self._wait()

        def _get_title():
            return self._get_css_str('.productTitle')

        def _get_image():
            return self._get_css_attr('.product-image img', 'src')

        def _get_toppings():
            return _get_description().replace("&", ",").split(",")

        def _get_description():
            self._wait_for_css('.product-desc')
            return self._get_css_str('.product-desc')

        def _get_price():
            return self._get_str_fl(self._get_css_str('#CurrentPrice'))

        def _size_count():
            return self._element_count('#OptionGroups_0__Options_0__list option')

        def _mark_crusts_unparsed():
            return self._script("""
                $("#OptionGroups_0__Options_0__OptionItems_2__Options_0__list_quantity_div label").addClass("unparsed")
            """)

        def _all_crusts_parsed():
            return self._element_count(".unparsed") == 0

        def _next_crust():
            return self._script('return $(".unparsed:first").removeClass("unparsed").text()')

        def _loop_crusts(size):
            _mark_crusts_unparsed()
            while not _all_crusts_parsed():
                _capture(_next_crust(), size)

        def _capture(crust, size):
            self._wait()
            self._new_pizza(
                _get_title(),
                _get_toppings(),
                size,
                _get_price(),
                crust,
                _get_image()
            )

        def _loop_sizes():
            for i in range(1, _size_count()):
                self._select_dropdown_option("OptionGroups_0__Options_0__list", i)
                _loop_crusts(["Small", "Medium", "Large"][i-1])

        def _parse_pizza_category(title):
            _select_pizza_category(title)
            for pizza_id in _get_ids():
                _follow_pizza_link(pizza_id)
                _loop_sizes()
                _select_pizza_category(title)

        _parse_pizza_category("Finest")
        _parse_pizza_category("Classics")
