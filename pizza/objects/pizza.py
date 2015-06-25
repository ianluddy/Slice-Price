
class Pizza():

    SLICES_PER_PERSON = 3

    def __init__(self, vendor_id, name, toppings, size, diameter, price, base, slices):
        self.vendor_id = vendor_id
        self.name = name
        self.toppings = toppings
        self.size = size
        self.diameter = diameter
        self.price = price
        self.base = base
        self.slices = slices

    def to_dict(self):
        return {
            "vendor_id": self.vendor_id,
            "name": self.name,
            "toppings": self.toppings,
            "size": self.size,
            "diameter": self.diameter,
            "base": self.base,
            "slices": self.slices,
            "price": self.price,
            "score": self._score(),
            "area": self._area(),
            "area_per_slice": self._area_per_slice(),
            "cost_psi": self._cost_per_square_inch(),
            "cost_per_slice": self._cost_per_slice(),
            "serves": self._serves()
        }

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