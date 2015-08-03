from time import sleep
from slice_scanner.objects.vendor import Vendor

class FourStar(Vendor):

    id = "Four Star Pizza"
    site = "https://www.fourstarpizza.ie"

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

    @staticmethod
    def complete_url(tail):
        return "https://weborder3.microworks.com%s" % tail

    def _get_meals(self):
        return []

    def _get_desserts(self):
        return []

    def _login(self):
        pass

    def _get_sides(self):
        return []

    def _get_pizzas(self):
        self.web_driver.get("https://weborder3.microworks.com/fourstar/Items/Index/1074")

        def _get_current_size():
            return self._get_str_int(self._script('return $("a.wcGroupsGroupName.wcGroupsCurrentGroup").text()'))

        def _get_next_pizza_page():
            return self._script("""
            return $("a.wcGroupsGroupName:contains(' Pizza'):first").removeClass("wcGroupsGroupName").attr("href")
            """)

        pages = []
        while self._element_count("a.wcGroupsGroupName:contains(' Pizza')") > 0:
            pages.append(self.complete_url(_get_next_pizza_page()))

        for page in pages:
            self.web_driver.get(page)

            while self._element_count(".wcItemsItemSelectItemButton") > 0:
                #try:
                self._select_next_by_class("wcItemsItemSelectItemButton")
                # except Exception:
                #     pass # js error always thrown here, it doesnt make a difference so lets ignore it

                self._wait_for_js()
                self._wait_for_js()

                self._wait_for_css("#wiItemDescription")

                self._new_pizza(
                    self._script('return $("#wiItemName").text()'),
                    self._script('return $("#wiItemDescription").text()').split(","),
                    _get_current_size(),
                    10.00, #_get_price(),
                    "Regular",
                    self.complete_url(self._script('return $("#wiItemImage img").attr("src")'))
                )

                # close the pizza dialog
                self._script('$(".ui-dialog-titlebar button").first().click()')
