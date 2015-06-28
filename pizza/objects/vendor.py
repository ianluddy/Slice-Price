import abc
import logging
from ..objects.pizza import Pizza
from ..utils import make_uuid

class Vendor():
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

    def _normalise_toppings(self, topping_list):
        return sorted([self._normalise_topping(topping) for topping in topping_list])

    def _normalise_topping(self, topping):
        return self.toppings[topping] if topping in self.toppings else topping

    def _diameter_from_size(self, size):
        return self.diameters.get(size, -1)

    def _slices_from_size(self, size):
        return self.slices.get(size, -1)

    def _new_pizza(self, name, toppings, size, diameter, price, base, slices):
        print "+PIZZA: %s %s %s %s %s %s %s" % (name, toppings, size, diameter, price, base, slices)
        return Pizza(self.id, name, self._normalise_toppings(toppings), size, diameter, price, base, slices)

    def get(self):

        def _get(func):
            try:
                return func()
            except Exception, e:
                logging.error("GET Error [%s] [%s]" % (self.name, str(func)), exc_info=True)

        return {
            "vendor": self.id,
            "pizza": _get(self._get_pizzas),
            "meals": _get(self._get_meals),
            "sides": _get(self._get_sides),
            "desserts": _get(self._get_desserts)
        }

    #### Implement ####

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

