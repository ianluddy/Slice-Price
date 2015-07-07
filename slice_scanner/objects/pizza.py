from ..utils import list_to_string
from hashlib import md5
from product import Product

class Pizza(Product):
    SLICES_PER_PERSON = 3

    # Crust normaliser. For converting "Thin & Crispy Crust" to "Thin"
    base_normaliser = {
        "Thin": ["thin"],
        "Stuffed": ["stuffed", "decadence"],
        "Italian": ["italian"],
        "Classic": ["classic"],
        "Gluten Free": ["gluten"],
    }

    # Toppings normaliser. For normalising "Smoked Bacon Rashers" to "Bacon"
    topping_normaliser = {
        "Bacon": ["smoked bacon rashers"],
        "Spinach": ["baby spinach"],
        "Tomatoes": ["sunblush baby tomatoes"],
        "Onions": ["red onions"],
        "Peppers": ["green and red peppers"],
        "Tomato Sauce": ["domino's own tomato sauce"],
        "Chicken": ["chicken breast strips"],
    }

    # Pizza style normaliser. For normalising "Vegi Supreme" to "Vegetarian"
    style_normaliser = {
        "Hawaiian": ["hawaiian"],
        "Hot": ["hot"],
        "BBQ": ["bbq"],
        "Vegetarian": ["veg"],
        "Meaty": ["meat"]
    }

    def __init__(self, **kwargs):
        super(Pizza, self).__init__(**kwargs)
        self.size = kwargs["size"]
        self.base = kwargs["base"]
        self.diameter = kwargs["diameter"]
        self.slices = kwargs["slices"]
        self.toppings = [self._normalise_data(self.topping_normaliser, topping) for topping in kwargs["toppings"]]
        self.style = self._normalise_data(self.style_normaliser, self.name)
        self.base_style = self._normalise_data(self.base_normaliser, self.base)
        self.description = self._description(self.base, kwargs["toppings"])

    def __str__(self):
        return "%s %s %s %s %s %s %s %s" % (
            self.vendor_id,
            self.name,
            self.base,
            self.toppings,
            self.style,
            self.price,
            self.size,
            self.diameter,
        )

    def _valid(self):
        valid = super(Pizza, self)._valid()
        for required in ["toppings", "size", "diameter", "base", "slices"]:
            if getattr(self, required) is None:
                return False
        return valid

    def _hash(self):
        return md5(self.vendor_id + self.name + self.size + self.base).hexdigest()

    def _description(self, base, toppings):
        return "%s Base with %s" % (
            base.replace("Crust", "").replace("Base", "").strip(),
            list_to_string(toppings)
        )

    def _score(self):
        # Overall score
        return ( float(self._area()) * float(len(self.toppings)) / float(self.price) ) * 100

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

    def to_dict(self):
        pizza_dict = super(Pizza, self).to_dict()
        if pizza_dict:
            for key in ["diameter", "slices", "base", "size", "toppings", "style", "base_style", "description"]:
                pizza_dict[key] = getattr(self, key)
            pizza_dict["area"] = self._area()
            pizza_dict["area_per_slice"] = self._area_per_slice()
            pizza_dict["cost_psi"] = self._cost_per_square_inch()
            pizza_dict["cost_per_slice"] = self._cost_per_slice()
            pizza_dict["serves"] = self._serves()
            return pizza_dict
        return None