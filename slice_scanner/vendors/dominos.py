from slice_scanner.objects.vendor import Vendor

class Dominos(Vendor):

    id = "Dominos Pizza"
    site = "http://www.dominos.ie"

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

    def _login(self):
        self.web_driver.get(self.site)
        self._script('$($("#store-finder-search select option").get(7)).prop("selected", "selected").trigger("change")')
        self._script('$("#store-finder-search .btn-primary").click()')
        self._wait_for_css(".store-details-row .btn-secondary")
        self._script('$(".store-details-row .btn-secondary").click()')

    def _get_sides(self):

        def _mark_sides_unparsed():
            self._script('$("#Sides .product").addClass("unparsed")')

        def _mark_side_parsed():
            self._script('$("#Sides .product.unparsed:first").removeClass("unparsed")')

        def _unparsed_sides_remaining():
            return self._element_count("#Sides .product.unparsed") > 0

        def _get_side_title():
            return self._get_css_str('#Sides .product.unparsed:first .product-title')

        def _get_side_image():
            return self._get_css_attr('#Sides .product.unparsed:first img', 'src')

        def _get_side_price():
            return self._get_str_fl(self._get_css_str('#Sides .product.unparsed:first .product-price'))

        while not self._element_count('#Sides .product'):
            self._wait()

        _mark_sides_unparsed()
        self._wait()
        while _unparsed_sides_remaining():
            self._new_side(
                _get_side_title(),
                _get_side_price(),
                _get_side_image(),
                _get_side_title()
            )
            _mark_side_parsed()
            self._wait()

    def _get_pizzas(self):

        def _mark_pizzas_unparsed(identifier):
            self._wait_for_css(identifier)
            self._script('$("%s").each(function(){$(this).addClass("unparsed")})' % identifier)

        def _get_next_unparsed_id():
            return self._script('return $(".product.unparsed:first").removeClass("unparsed").attr("data-productid")')

        def _all_products_parsed():
            return self._script('return $(".product.unparsed").length') == 0

        def _get_product_img(product_id):
            identifier = ".pizza.product[data-productid='%s'] .product-image" % product_id
            return self._script('return $("%s").attr("lazy-src").toString();' % identifier)

        def _get_product_links():
            product_links = {}
            while not _all_products_parsed():
                product_id = _get_next_unparsed_id()
                product_links[product_id] = _get_product_img(product_id)
            return product_links

        def _follow_product_link(product_id):
            self._script('$(".pizza.product[data-productid=%s] button").click()' % product_id)

        def _return_to_menu():
            self.web_driver.get("%s/menu" % self.site)
            self._wait_for_alert(timeout=0.5)
            self._wait_for_alert_to_clear(timeout=0.5)

        def _get_pizza_title():
            self._wait_for_css("h1.pizza-name")
            return self._script('return $("h1.pizza-name").first().text()')

        def _get_pizza_toppings():
            self._wait_for_css(".topping")
            toppings = []
            for i in range( self._script('return $(".topping.is-selected").length') ):
                toppings.append(self._script('return $($(".topping.is-selected").get(%s)).text()' % i).strip())
            return toppings

        def _size_count():
            self._wait_for_css("li.pizza-size")
            return self._script('return $("li.pizza-size").length')

        def _choose_size(index):
            return self._script('return $($("li.pizza-size").get(%s)).click().text()' % index).strip().split(" ")[0]

        def _get_price():
            return self._script('return $(".pizza-price:first").text()')[1:]

        def _crust_count():
            self._wait_for_css(".carousel-content.product")
            return self._script('return $(".carousel-content .product").length')

        def _choose_crust(index):
            return self._script(
                'return $($(".carousel-content .product").get(%s)).click().find("p.product-title").text()'
                % index
            )

        _mark_pizzas_unparsed("[id='Speciality Pizzas'] .pizza")
        _mark_pizzas_unparsed("[id='Gourmet Pizzas'] .pizza")

        for product_id, product_img in _get_product_links().iteritems():
            _follow_product_link(product_id)
            toppings = _get_pizza_toppings()
            title = _get_pizza_title()
            for i in range(_size_count()):
                size = _choose_size(i)
                self._wait()
                for j in range(_crust_count()):
                    crust = _choose_crust(j)
                    self._wait()
                    self._new_pizza(title, toppings, size, _get_price(), crust, product_img)
                _choose_crust(0)

            _return_to_menu()
