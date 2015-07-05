from product import Product
from hashlib import md5

class Side(Product):

    def __str__(self):
        return "Side - %s %s %s" % (
            str(self.name),
            self.price,
            self.quantity,
        )

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
        return md5(self.vendor_id + self.name + self.size + self.base).hexdigest()

    def _score(self):
        return 10
