from parser import Parser

class Dominos(Parser):

    def get_pizzas(self):
        return [
            {
                "name": "Mighty Meaty",
                "toppings": ["pepperoni", "ham"],
                "size": "Large",
                "diameter": "16",
                "base": "thin",
                "price": 12.5
            },
            {
                "name": "Hawaiian",
                "toppings": ["pineapple", "ham"],
                "size": "Large",
                "diameter": "16",
                "base": "thin",
                "price": 12.5
            },
            {
                "name": "Mighty Meaty",
                "toppings": ["pepperoni", "ham"],
                "size": "medium",
                "diameter": "12",
                "base": "thin",
                "price": 11.5
            },
            {
                "name": "Hawaiian",
                "toppings": ["pineapple", "ham"],
                "size": "medium",
                "diameter": "12",
                "base": "thin",
                "price": 11.5
            },
        ]

    def get_meals(self):
        return []

    def get_sides(self):
        return []

    def get_desserts(self):
        return []