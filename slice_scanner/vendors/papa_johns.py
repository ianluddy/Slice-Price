# coding=utf-8
from slice_scanner.objects.vendor import Vendor

class PapaJohns(Vendor):

    id = "Papa Johns"
    site = "http://www.papajohns.co.uk"

    diameter_reference = {
        "small": 10,
        "medium": 12,
        "large": 14,
        "xxl": 16
    }

    slice_reference = {
        "small": 4,
        "medium": 6,
        "large": 10,
        "xxl": 10
    }

    def _get_meals(self):
        return []

    def _get_desserts(self):
        return []

    def _get_sides(self):
        return []

    def _get_pizzas(self):

        def _get_pizza_count():
            return int(self._script('return $(".menuList").length'))

        def _get_selected_title(index):
            return self._script('return $($(".menuList").get(%s)).find("h3").text()' % index).strip()

        def _get_selected_img(index):
            return self._script('return $($(".menuList")[%s]).find("img")[0]["src"]' % index).strip()

        def _get_selected_toppings(index):
            return self._script(
                'return $($(".menuList").get(%s)).find("p.description").text()' % index
            ).strip().replace("& ", ",").replace("and ", ",").replace("More info", "").replace(".", "").split(", ")

        def _mark_options_unparsed(index):
            return self._script('$($(".menuList").get(%s)).find("select option").addClass("unparsed")' % index)

        def _unparsed_options_remaining(index):
            return self._script('return $($(".menuList").get(%s)).find("select option.unparsed").length' % index) > 0

        def _get_next_option(index):
            return self._script(
                'return $($(".menuList").get(%s)).find("select option.unparsed:first").removeClass("unparsed").text()'
                % index
            ).lower().replace(" ", "").split(",")

        for i in range(_get_pizza_count()):
            name = _get_selected_title(i)
            toppings = _get_selected_toppings(i)
            img = _get_selected_img(i)
            _mark_options_unparsed(i)
            while _unparsed_options_remaining(i):
                base, size, price = _get_next_option(i)
                self._new_pizza(name, toppings, size, price, base, img)

    def _login(self):
        self.web_driver.get("http://www.papajohns.co.uk/stores/battersea/pizzas.aspx")