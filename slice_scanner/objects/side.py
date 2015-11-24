from product import Product
from hashlib import md5

class Side(Product):

    # Sides normaliser. For converting "Frank's RedHot Wings" to "Chicken"
    side_normaliser = {
        "Combo": ["mix box", "combo"],
        "Chicken": ["wing", "chick", "kicker"],
        "Dip": ["dip"],
        "Fries": ["fries", "fry"],
        "Garlic Bread": ["garlic pizza", "garlic bread"],
        "Dough Balls": ["dough ball"],
        "Potato Wedges": ["potato", "wedge"],
        "Nachos": ["nacho"],
        "Coleslaw": ["slaw"],
        "Pasta": ["pasta", "macaroni"],
        "Cheese": ["cheese triangle"],
    }

    def __init__(self, **kwargs):
        super(Side, self).__init__(**kwargs)
        self.type = self._normalise_data(self.side_normaliser, self.name)

    def __str__(self):
        return "%s %s %s %s %s" % (
            self.vendor,
            self.name,
            self.type,
            self.price,
            self.quantity
        )

    def _valid(self):
        valid = super(Side, self)._valid()
        for required in ["quantity"]:
            if getattr(self, required) is None:
                return False
        return valid

    def _hash(self):
        return md5(self.vendor + self.name + str(self.quantity)).hexdigest()

    def to_dict(self):
        side_dict = super(Side, self).to_dict()
        if side_dict:
            for key in ["quantity", "type"]:
                side_dict[key] = getattr(self, key)
            return side_dict
        return None