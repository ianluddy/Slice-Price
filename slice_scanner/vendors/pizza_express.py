from slice_scanner.objects.vendor import Vendor

class PizzaExpress(Vendor):

    id = "pizza_express"
    name = "Pizza Express"
    site = "https://http://www.pizzaexpress.com/"

    diameter_reference = {
    }

    slice_reference = {
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