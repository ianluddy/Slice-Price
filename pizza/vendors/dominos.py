from pizza.objects.vendor import Vendor

class Dominos(Vendor):

    toppings = {
        "Smoked Bacon Rashers": "bacon",
        "Baby Spinach": "spinach"
    }

    def get_pizzas(self):
        return [
            self._new_pizza("Mighty Meaty", ["pepperoni", "ham"], "large", 16, 12.5, "thin", 12),
            self._new_pizza("Hawaiian", ["pepperoni", "ham"], "large", 16, 12.5, "thin", 12),
        ]

    def get_meals(self):
        return []

    def get_sides(self):
        return []

    def get_desserts(self):
        return []