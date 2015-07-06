from product import Product
from hashlib import md5

class Side(Product):

    # Sides normaliser. For converting "Frank's RedHot Wings" to "Chicken"
    side_normaliser = {
        "Combo": ["mix box", "combo"],
        "Dip": ["dip"],
        "Chicken": ["wing", "chick", "kicker"],
        "Garlic Bread": ["garlic pizza bread"],
        "Dough Balls": ["dough ball"],
        "Potato Wedges": ["potato", "wedge"],
        "Nachos": ["nacho"],
        "Coleslaw": ["slaw"],
    }

    def __init__(self, **kwargs):
        super(Side, self).__init__(**kwargs)
        self.type = self._normalise_data(self.side_normaliser, self.name)
        self.quantity = kwargs["quantity"]

    def __str__(self):
        return "%s %s %s %s %s" % (
            self.vendor_id,
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
        return md5(self.vendor_id + self.name + str(self.quantity)).hexdigest()

    def _score(self):
        return float(self.quantity) / float(self.price) * 100

    def to_dict(self):
        side_dict = super(Side, self).to_dict()
        if side_dict:
            for key in ["quantity", "type"]:
                side_dict[key] = getattr(self, key)
            return side_dict
        return None