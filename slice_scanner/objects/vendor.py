import abc
from ..objects.parser import Parser
from ..objects.pizza import Pizza
from ..objects.side import Side
from ..utils import wrapped_execute

class Vendor(Parser):
    __metaclass__ = abc.ABCMeta
    id = None
    name = None
    site = None

    # Diameter dict. For converting "large" to 13.5
    diameter_reference = {}

    # Slice dict. For converting "large" to 10
    slice_reference = {}

    def __init__(self, outgoing_queue):
        self.queue = outgoing_queue # Queue for stuff we've parsed

    def _new_product(self, product, **kwargs):
        new_product = wrapped_execute(lambda: product(**self._normalise_parsed_data(kwargs)))
        if new_product:
            self.queue.put(new_product)

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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "site": self.site
        }

    def _diameter_from_size(self, size):
        return self.diameter_reference.get(size, -1)

    def _slices_from_size(self, size):
        return self.slice_reference.get(size, -1)

    def _new_pizza(self, name, toppings, size, price, base, img):
        slices = self._slices_from_size(size)
        diameter = self._diameter_from_size(size)
        self._new_product(
            Pizza, vendor_id=self.id, name=name, toppings=toppings, size=size,
            diameter=diameter, price=price, base=base, slices=slices, img=img
        )

    def _new_side(self, name, price, size, quantity, img, description=None):
        self._new_product(
            Side, vendor_id=self.id, name=name, price=price, size=size, quantity=quantity,
            img=img, description=description
        )

    def parse(self):
        self._login()
        wrapped_execute(self._get_pizzas)
        wrapped_execute(self._get_sides)
        wrapped_execute(self._get_desserts)
        wrapped_execute(self._get_meals)

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
