from ..utils import list_to_title_string, float_to_two_places
from hashlib import md5
from product import Product

class Pizza(Product):
    SLICES_PER_PERSON = 3

    # Crust normaliser. For converting "Thin & Crispy Crust" to "Thin"
    base_normaliser = {
        "Thin": ["thin"],
        "Stuffed": ["stuffed", "decadence", "cheesy bites"],
        "Italian": ["italian"],
        "Pan": ["classic", "pan", "original"], # TODO = verify that classic and pan are the same thing
        "Gluten Free": ["gluten"],
    }

    # Toppings normaliser. For normalising "Smoked Bacon Rashers" to "Bacon", and "Spicy Minced Beef" to "Beef"
    topping_normaliser = {
        "Aubergines": ["aubergine"],
        "BBQ Sauce": ["bbq"],
        "Tomato Sauce": ["domino's own tomato sauce"],
        "Bacon": ["bacon"],
        "Spinach": ["spinach"],
        "Onion Bhaji": ["bhaji"],
        "Onions": ["onion"],
        "Sausage": ["sausage"],
        "Olives": ["olives"],
        "Pineapple": ["pineapple"],
        "Chillies": ["chilli"],
        "Ham": ["ham"],
        "Mushrooms": ["mushrooms"],
        "Peppers": ["red peppers", "mixed peppers", "green peppers"],
        "Tomatoes": ["tomatoes", "tomato", "sunblush"],
        "Chicken": ["chicken breast strips", "chargrilled chicken"],
        "Jalapenos": ["jalap"],
        "Pepperoni": ["pepperoni"],
        "Beef": ["beef"],
        "Pork": ["pork"],
        "Pesto": ["pesto"],
        "Piri": ["piri"],
        "Sweetcorn": ["sweetcorn"],
        "Tandoori Chicken": ["tandoori chicken"],
        "Pepper Confit": ["pepper confit"],
        "Create your own": ["freestyle", "create"], # TODO - put this somewhere else
    }

    # Toppings we don't care about
    ignored_toppings = [
        "cheese",
        "seasoning",
        "herbs",
    ]

    # Sauce normaliser.
    sauce_normaliser = {
        "BBQ Sauce": ["bbq"],
        "Tomato Sauce": ["tomato"]
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
        toppings, sauce = self._organise_toppings(self._clean_toppings(kwargs["toppings"]))
        self.sauce = self._normalise_data(self.sauce_normaliser, sauce)
        self.toppings = [self._normalise_data(self.topping_normaliser, topping) for topping in toppings]
        self.style = self._normalise_data(self.style_normaliser, self.name)
        self.base_style = self._normalise_data(self.base_normaliser, self.base)
        self.description = self._description(self.base, kwargs["toppings"])

    def __str__(self):
        return "%s %s %s %s %s %s %s %s %s" % (
            self.vendor,
            self.name,
            self.base,
            [t for t in self.toppings],
            self.style,
            self.price,
            self.size,
            self.diameter,
            self.img,
        )

    @staticmethod
    def _organise_toppings(topping_list):
        toppings = []
        sauce = "tomato" # assume tomato unless we find some saucy info
        for topping in topping_list:
            if "sauce" in topping.lower():
                sauce = topping
            else:
                toppings.append(topping)
        return toppings, sauce

    def _clean_toppings(self, topping_list):
        toppings = []
        for topping in topping_list:
            ignore = False
            for ignored in self.ignored_toppings:
                if ignored in topping.lower():
                    ignore = True
            if not ignore:
                toppings.append(topping)
        return toppings

    def _valid(self):
        valid = super(Pizza, self)._valid()
        for required in ["toppings", "size", "diameter", "base", "slices"]:
            if getattr(self, required) is None:
                return False
        return valid

    def _hash(self):
        to_hash = u""
        to_hash += self.vendor
        to_hash += self.name
        to_hash += self.size
        to_hash += self.base
        return md5(to_hash).hexdigest()

    def _description(self, base, toppings):
        return "%s Base with %s." % (
            base.lower().replace("crust", "").replace("base", "").strip().title(),
            list_to_title_string(toppings)
        )

    def _score(self):
        # Overall score (area * toppings[incl cheese] / price)
        return int(( float(self._area()) * float(len(self.toppings) + 1) / float(self.price) ) * 10)

    def _area(self):
        # Area in square inches
        return float_to_two_places(((self.diameter / 2.0) ** 2 ) * 3.14)

    def _area_per_slice(self):
        # Slice area in square inches
        return float_to_two_places(float(self._area()) / self.slices)

    def _serves(self):
        # Number of people satisfied
        return int(float(self.slices) / self.SLICES_PER_PERSON)

    def _cost_per_slice(self):
        # Cost per slice
        return float_to_two_places(float(self.price) / self.slices)

    def _cost_per_square_inch(self):
        # Cost per square inch
        return float_to_two_places(float(self.price) / self._area())

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