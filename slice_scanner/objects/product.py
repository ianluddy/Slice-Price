import abc
from time import time

class Product():
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        self.vendor_id = kwargs["vendor_id"]
        self.name = kwargs["name"]
        self.price = kwargs["price"]
        self.description = kwargs.get("description")
        self.quantity = kwargs.get("quantity", 1)

    def __str__(self):
        return "%s %s %s %s %s" % (
            self.category,
            self.type,
            self.name,
            self.price,
            self.quantity
        )

    def to_dict(self):
        if self._valid():
            product_dict = {}
            product_dict["vendor_id"] = self.vendor_id
            product_dict["name"] = self.name
            product_dict["price"] = self.price
            product_dict["category"] = self.category
            product_dict["type"] = self.type
            product_dict["description"] = self.description
            product_dict["stamp"] = time()
            product_dict["hash"] = self._hash()
            product_dict["score"] = self._score()
            return product_dict
        return None

    def _valid(self):
        for required in ["name", "price", "vendor_id", "type", "category"]:
            if getattr(self, required) is None:
                return False
        return True

    @abc.abstractmethod
    def _hash(self):
        """ Get product hash """

    @abc.abstractmethod
    def _score(self):
        """ Get product hash """