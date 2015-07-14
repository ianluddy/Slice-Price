from time import sleep
from slice_scanner.objects.vendor import Vendor

class Dominos(Vendor):

    id = "Dominos Pizza"
    site = "https://www.dominos.ie"

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
        self.web_driver.get(self.site)
        self._script('$($("#store-finder-search select option").get(7)).prop("selected", "selected").trigger("change")')
        self._script('$("#store-finder-search .btn-primary").click()')
        self._wait_for_css(".store-details-row .btn-secondary")
        self._script('$(".store-details-row .btn-secondary").click()')

    #### Sides ####

    def _get_sides(self):
        return []

        self.web_driver.get("%s/menu" % self.site)
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
                    name, price, size, quantity, None, description
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
                self._wait_for_js()
                for j in range(_crust_count()):
                    crust = _choose_crust(j)
                    self._wait_for_js()
                    self._new_pizza(title, toppings, size, _get_price(), crust, product_img)
                _choose_crust(0)

            _return_to_menu()
