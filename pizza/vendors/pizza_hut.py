class Dominos(Vendor, Parser):

    toppings = {
        "smoked bacon rashers": "bacon",
        "baby spinach": "spinach",
        "sunblush baby tomatoes": "tomatoes"
    }

    diameters = {
        "large": 13.5,
        "medium": 11.5,
        "small": 9.5,
        "personal": 7
    }

    slices = {
        "large": 10,
        "medium": 8,
        "small": 6,
        "personal": 4
    }

    def _get_pizzas(self):
        return []

    def _get_meals(self):
        return []

    def _get_sides(self):
        return []

    def _get_desserts(self):
        return []