import abc
import logging

from ..objects.parser import Parser
from ..objects.pizza import Pizza
from ..objects.side import Side
from ..utils import make_uuid, wrapped_execute

class Vendor(Parser):
    __metaclass__ = abc.ABCMeta

    # Toppings normaliser. For normalising "Smoked Bacon Rashers" to "bacon"
    toppings = {}

    # Diameter dict. For converting "large" to 13.5
    diameters = {}

    # Slice dict. For converting "large" to 10
    slices = {}

    def __init__(self):
        self.name = self.__class__.__name__
        self.id = make_uuid(self.__class__.__name__)
        self._reset_data()

    def _reset_data(self):
        self.pizzas = []
        self.sides = []
        self.desserts = []
        self.meals = []

    def _normalise_toppings(self, topping_list):
        return sorted([self._normalise_topping(topping) for topping in topping_list])

    def _normalise_topping(self, topping):
        return self.toppings[topping] if topping in self.toppings else topping

    def _diameter_from_size(self, size):
        return self.diameters.get(size, -1)

    def _slices_from_size(self, size):
        return self.slices.get(size, -1)

    # def _new_pizza(self, name, toppings, size, diameter, price, base, slices):
    #     new_pizza = wrapped_execute(lambda: Pizza(vendor_id=self.id, name=name,
    #                                               toppings=self._normalise_toppings(toppings), size=size,
    #                                               diameter=diameter, price=price, base=base, slices=slices))
    #     if new_pizza:
    #         print str(new_pizza)
    #         self.pizzas.append(new_pizza)

    def _new_pizza(self, name, toppings, size, diameter, price, base, slices):
        self._new_product(
            self.pizzas, Pizza, vendor_id=self.id, name=name, toppings=self._normalise_toppings(toppings), size=size,
            diameter=diameter, price=price, base=base, slices=slices
        )

    def _new_side(self, name, price, size, quantity):
        self._new_product(self.sides, Side, name=name, price=price, size=size, quantity=quantity)

    def _new_product(self, group, product, **kwargs):
        new_product = wrapped_execute(lambda: product(**kwargs))
        if new_product:
            print str(new_product)
            group.append(new_product)

    def parse(self):
        self._reset_data()
        self._login()

        wrapped_execute(self._get_pizzas)
        wrapped_execute(self._get_desserts)
        wrapped_execute(self._get_sides)
        wrapped_execute(self._get_meals)

        return {
            "vendor": self.id,
            "pizza": self.pizzas,
            "meals": self.meals,
            "sides": self.sides,
            "desserts": self.desserts
        }

    #### Implement ####

    @abc.abstractmethod
    def _login(self):
        """ Login to site, set address etc. """

    @abc.abstractmethod
    def _get_pizzas(self):
        """ Get list of Pizzas """

    @abc.abstractmethod
    def _get_meals(self):
        """ Get list of Meals """

    @abc.abstractmethod
    def _get_sides(self):
        """ Get list of Sides """

    @abc.abstractmethod
    def _get_desserts(self):
        """ Get list of Desserts """
