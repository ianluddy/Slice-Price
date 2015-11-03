from time import sleep
from slice_scanner.objects.vendor import Vendor

class FourStar(Vendor):

    id = "Four Star Pizza"
    site = "https://www.fourstarpizza.ie"

    slice_reference = { # TODO - verify these
        16: 10,
        12: 8,
        9: 6,
        7: 4
    }

    @staticmethod
    def complete_url(tail):
        return "https://weborder3.microworks.com%s" % tail if tail else None

    def _get_meals(self):
        return []

    def _get_desserts(self):
        return []

    def _login(self):
        pass

    def _get_sides(self):

        def _next_side_type():
            return self._script("""
                return $(".wcGroupsSubGroupList .wcGroupsGroupName:first").removeClass("wcGroupsGroupName").attr("href")
            """)

        def _unparsed_side_types():
            return self._element_count('.wcGroupsSubGroupList .wcGroupsGroupName') > 0

        def _unparsed_sides():
            return self._element_count('.wcItemsItem:visible') > 0

        def _side_parsed():
            self._script('$(".wcItemsItem:visible:first").removeClass("wcItemsItem")')

        def _get_name():
            side_name = self._get_css_str(".wcItemsItem:visible:first .wcItemsItemName")
            if _chicken_side() and not 'chicken' in side_name.lower():
                return side_name + ' Chicken'
            return side_name

        def _get_description():
            return self._get_css_str(".wcItemsItem:visible:first .wcItemsItemDescription")

        def _get_price():
            return self._get_str_fl(self._get_css_str(".wcItemsItem:visible:first .wcItemsItemPrice"))

        def _get_image():
            return self.complete_url(self._get_css_attr(".wcItemsItem:visible:first .wcItemsItemThumb img", "src"))

        def _chicken_side():
            return 'chicken' in self._get_css_str('.wcGroupsGroup.wcGroupsCurrentGroup .wcGroupsGroupName').lower()

        self.web_driver.get("https://weborder3.microworks.com/fourstar/Items/Index/1012")

        pages = []
        while _unparsed_side_types():
            pages.append(self.complete_url(_next_side_type()))

        for page in pages:
            self.web_driver.get(page)
            while _unparsed_sides():
                self._new_side(_get_name(), _get_price(), _get_image(), _get_description())
                _side_parsed()

    def _get_pizzas(self):

        self.web_driver.get("https://weborder3.microworks.com/fourstar/Items/Index/1074")

        def _get_current_size():
            return self._get_str_int(self._script('return $("a.wcGroupsGroupName.wcGroupsCurrentGroup").text()'))

        def _gluten_free():
            return "gluten" in self._script('return $("a.wcGroupsGroupName.wcGroupsCurrentGroup").text()').lower()

        def _get_current_toppings():
            toppings = self._get_css_str("#wiItemDescription").replace("&", ",").replace("\n", "").replace("\t", "")\
                .replace("-", "").replace("  ", " ").split(",")
            return [t for t in toppings if t not in ["", " "]]

        def _get_current_price():
            self._wait_for_css(".wcItemPrice")
            return self._get_str_fl(self._script('return $(".wcItemPrice").first().text()'))

        def _get_next_pizza_page():
            return self._script("""
            return $("a.wcGroupsGroupName:contains(' Pizza'):first").removeClass("wcGroupsGroupName").attr("href")
            """)

        def _select_crust_tab():
            self._script("""
            $(".wcItemModifierListTab").first().children("a").click();
            $(".wcItemModifierListTab:contains('Base')").children("a").click();
            """)

        def _get_next_crust():
            return self._script("""
            return $(".wcItemModifierLabel:visible:first").removeClass("wcItemModifierLabel").children("label").text()
            """)

        pages = []
        while self._element_count("a.wcGroupsGroupName:contains(' Pizza')") > 0:
            pages.append(self.complete_url(_get_next_pizza_page()))

        for page in pages:
            self.web_driver.get(page)

            while self._element_count(".wcItemsItemSelectItemButton") > 0:
                self._wait()
                self._select_next_by_class("wcItemsItemSelectItemButton")
                self._wait()
                self._wait_for_css("#wiItemDescription")

                toppings = _get_current_toppings()
                size = _get_current_size()
                self._wait()
                price = _get_current_price()
                image = self.complete_url(self._script('return $("#wiItemImage img").attr("src")'))
                title = self._script('return $("#wiItemName").text()')

                _select_crust_tab()
                self._wait()
                self._wait()
                if _gluten_free():
                    self._new_pizza(title, toppings, size, price, "Gluten Free", image)
                else:
                    while self._element_count(".wcItemModifierLabel:visible") > 0:
                        self._new_pizza(title, toppings, size, price, _get_next_crust(), image)

                self._script('$(".ui-dialog-titlebar button").first().click()')
                self._wait()


