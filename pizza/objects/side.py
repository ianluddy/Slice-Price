from product import Product
from hashlib import md5

class Side(Product):

    def __init__(self, **kwargs):
        super(Side, self).__init__(**kwargs)
        self.category = "side"
        self.type = kwargs["type"]
        self.quantity = kwargs["quantity"]

    def to_dict(self):
        side_dict = super(Side, self).to_dict()
        if side_dict:
            side_dict["quantity"] = self.quantity
            return side_dict
        return None

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
