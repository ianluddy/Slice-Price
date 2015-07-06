import abc
from ..objects.parser import Parser
from ..objects.pizza import Pizza
from ..objects.side import Side
from ..utils import wrapped_execute

class Vendor(Parser):
    __metaclass__ = abc.ABCMeta

    # Vendor information
    id = None
    name = None
    site = None

    # Diameter dict. For converting "large" to 13.5
    diameter_reference = {}

    # Slice dict. For converting "large" to 10
    slice_reference = {}

    @staticmethod
    def _new_product(group, product, **kwargs):
        new_product = wrapped_execute(lambda: product(**kwargs))
        if new_product:
            print str(new_product)
            group.append(new_product)

    @staticmethod
    def _normalise_data(normaliser, data):
        data = data.lower()
        if data in normaliser:
            return data
        for key, values in normaliser.iteritems():
            for value in values:
                if value in data:
                    return key
        return data

    def __init__(self):
        self._reset_data()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "site": self.site
        }

    def _reset_data(self):
        self.pizzas = []
        self.sides = []
        self.desserts = []
        self.meals = []

    def _diameter_from_size(self, size):
        return self.diameter_reference.get(size, -1)

    def _slices_from_size(self, size):
        return self.slice_reference.get(size, -1)

    def _new_pizza(self, name, toppings, size, diameter, price, base, slices):
        self._new_product(
            self.pizzas, Pizza, vendor_id=self.id, name=name, toppings=toppings, size=size,
            diameter=diameter, price=price, base=base, slices=slices
        )

    def _new_side(self, name, price, size, quantity, description=None):
        self._new_product(
            self.sides, Side, vendor_id=self.id, name=name, price=price, size=size, quantity=quantity,
            description=description
        )

    def parse(self):
        self._reset_data()
        self._login()

        wrapped_execute(self._get_pizzas)
        wrapped_execute(self._get_sides)
        # wrapped_execute(self._get_desserts)
        # wrapped_execute(self._get_meals)

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
