from hashlib import md5
from product import Product

class Pizza(Product):
    SLICES_PER_PERSON = 3

    def __init__(self, **kwargs):
        super(Pizza, self).__init__(**kwargs)
        self.category = "pizza"
        self.type = "pizza"
        self.size = kwargs["size"]
        self.base = kwargs["base"]
        self.toppings = kwargs["toppings"]
        self.diameter = kwargs["diameter"]
        self.slices = kwargs["slices"]

    def to_dict(self):
        pizza_dict = super(Pizza, self).to_dict()
        if pizza_dict:
            pizza_dict["diameter"] = self.diameter
            pizza_dict["toppings"] = self.toppings
            pizza_dict["slices"] = self.slices
            pizza_dict["base"] = self.base
            pizza_dict["size"] = self.size
            pizza_dict["area"] = self._area()
            pizza_dict["area_per_slice"] = self._area_per_slice()
            pizza_dict["cost_psi"] = self._cost_per_square_inch()
            pizza_dict["cost_per_slice"] = self._cost_per_slice()
            pizza_dict["serves"] = self._serves()
            return pizza_dict
        return None

    def _valid(self):
        valid = super(Pizza, self)._valid()
        for required in ["toppings", "size", "diameter", "base", "slices"]:
            if getattr(self, required) is None:
                return False
        return valid

    def _hash(self):
        return md5(self.vendor_id + self.name + self.size + self.base).hexdigest()

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