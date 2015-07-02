from time import time
from hashlib import md5

class Pizza():

    SLICES_PER_PERSON = 3
    ATTRIBUTES = ["vendor_id", "name", "toppings", "size", "diameter", "price", "base", "slices"]

    def __init__(self, **kwargs):
        for mandatory in self.ATTRIBUTES:
            assert kwargs.get(mandatory), "%s missing" % str(mandatory)
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def to_dict(self):
        pizza_dict = {
            "score": self._score(),
            "area": self._area(),
            "area_per_slice": self._area_per_slice(),
            "cost_psi": self._cost_per_square_inch(),
            "cost_per_slice": self._cost_per_slice(),
            "serves": self._serves(),
            "hash": md5(self.vendor_id + self.name + self.size + self.base).hexdigest(),
            "stamp": time()
        }
        for mandatory in self.ATTRIBUTES:
            pizza_dict[mandatory] = getattr(self, mandatory)
        return pizza_dict

    def _score(self):
        # Overall score
        return ( float(self.diameter) * float(len(self.toppings)) / float(self.price) ) * 100

    def _area(self):
        # Area in square inches
        return ((self.diameter / 2.0) ** 2 ) * 3.14

    def _area_per_slice(self):
        # Slice area in square inches
        return float(self._area()) / self.slices

    def _serves(self):
        # Number of people satisfied
        return float(self.slices) / self.SLICES_PER_PERSON

    def _cost_per_slice(self):
        # Cost per slice
        return float(self.price) / self.slices

    def _cost_per_square_inch(self):
        # Cost per square inch
        return float(self.price) / self._area()