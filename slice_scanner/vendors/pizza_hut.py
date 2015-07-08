from slice_scanner.objects.vendor import Vendor

class PizzaHut(Vendor):

    id = "pizza_hut"
    name = "Pizza Hut"
    site = "https://www.pizzahut.co.uk/"

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

    def _get_sides(self):
        return []

    def _get_pizzas(self):
        return []

    def _login(self):
        return None