from slice_scanner.objects.vendor import Vendor

class PizzaHut(Vendor):

    id = "Pizza Hut"
    site = "http://www.pizzahutdelivery.ie"

    diameter_reference = {
        "large": 13.5,
        "regular": 11.5,
        "medium": 11.5,
        "small": 9,
        "personal": 7
    }

    slice_reference = {
        "large": 10,
        "regular": 8,
        "medium": 8,
        "small": 6,
        "personal": 4
    }

    def _login(self):
        self.web_driver.get("http://www.pizzahutdelivery.ie/order-online.php?location_id=2633&method=delivery")
        self._wait()

    def _get_sides(self):

        def _select_type(side_type):
            self._wait()
            self._script('$("a[data-category-name*=\'%s\']").click()' % side_type)
            self._wait()

        def _mark_unparsed():
            self._script('$(".m2g-menu-product:visible").addClass("unparsed")')

        def _all_parsed():
            return self._script('return $(".m2g-menu-product.unparsed:visible").length') == 0

        def _mark_parsed():
            self._script('$(".m2g-menu-product.unparsed:visible:first").removeClass("unparsed")')

        def _get_price():
            return self._get_str_fl(self._get_css_str('.m2g-menu-product.unparsed:visible:first .m2g-menu-product-price'))

        def _get_name():
            return self._get_css_str('.m2g-menu-product.unparsed:visible:first .m2g-menu-product-name')

        def _get_description():
            return self._get_css_str('.m2g-menu-product.unparsed:visible:first .m2g-menu-product-description')

        def _get_image():
            return self._get_css_attr('.m2g-menu-product.unparsed:visible:first .m2g-menu-product-image', 'src')

        def _parse_next():
            self._new_side(_get_name(), _get_price(), _get_image(), _get_description())

        def _parse_visible():
            _mark_unparsed()
            while not _all_parsed():
                _parse_next()
                _mark_parsed()

        def _parse_side_page(title):
            _select_type(title)
            _parse_visible()

        _parse_side_page("Classic Sides")
        _parse_side_page("Premium Sides")

    def _get_pizzas(self):

        def _select_size(size):
            self._script('$("a[data-category-name=\'%s\']").click()' % size)
            self._wait()

        def _get_current_pizzas():
            _mark_unparsed()
            while not _all_parsed():
                _parse_next()

        def _mark_unparsed():
            self._script('$(".m2g-menu-product button:visible").addClass("unparsed")')

        def _all_parsed():
            return self._script('return $(".m2g-menu-product button.unparsed:visible").length') == 0

        def _get_price():
            return self._get_str_fl(self._get_css_str('.m2g-product-editor-price'))

        def _get_toppings():
            toppings = self._get_css_str(".m2g-product-editor-product-description").replace("\n", "").replace("-", "")\
                .replace("  ", " ").split(",")
            return [t for t in toppings if t not in ["", " "]]

        def _get_name():
            return self._get_css_str('.m2g-product-editor-product-name').split("(")[0]

        def _get_size():
            return self._get_css_str('.m2g-product-editor-product-name').replace(")", "").split("(")[1].lower()

        def _get_image():
            return self._get_css_attr('.m2g-product-editor-product-image', 'src')

        def _mark_bases_unparsed():
            self._script('$("div:visible[data-modifier-group-name*=\'Base\'] div.m2g-icon--checkbox").addClass("unparsed")')

        def _all_bases_parsed():
            return self._script('return $("div:visible[data-modifier-group-name*=\'Base\'] div.m2g-icon--checkbox.unparsed").length') == 0

        def _parse_next_base():
            self._script('$("div:visible[data-modifier-group-name*=\'Base\'] div.m2g-icon--checkbox.unparsed").first().click().removeClass("unparsed")')
            self._wait()
            base = self._script('return $("div:visible[data-modifier-group-name*=\'Base\'] div.m2g-touchable[data-selection-state=on]").attr("data-modifier-name")')
            if not base:
                base = self._script('return $("div:visible[data-modifier-group-name*=\'Base\'] div.m2g-touchable[data-selection-state=off]").first().attr("data-modifier-name")')
            return base.split("] ")[1]

        def _parse_next():
            self._script('$(".m2g-menu-product button.unparsed:visible").first().click().removeClass("unparsed")')
            self._wait()

            _mark_bases_unparsed()

            name = _get_name()
            size = _get_size()
            toppings = _get_toppings()
            image = _get_image()

            while not _all_bases_parsed():
                base = _parse_next_base()
                self._new_pizza(name, toppings, size, _get_price(), base, image)

            self._script('$("button.m2g-modal-close-button").click()')
            self._wait()

        _select_size("Personal Pizzas")
        _get_current_pizzas()
        _select_size("Regular Pizzas")
        _get_current_pizzas()
        _select_size("Medium Pizzas")
        _get_current_pizzas()
        _select_size("Large Pizzas")
        _get_current_pizzas()