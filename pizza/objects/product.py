import abc
from time import time

class Product():
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        self.vendor_id = kwargs["vendor_id"]
        self.name = kwargs["name"]
        self.price = kwargs["price"]

    def to_dict(self):
        if self._valid():
            product_dict = {}
            product_dict["vendor_id"] = self.vendor_id
            product_dict["name"] = self.name
            product_dict["price"] = self.price
            product_dict["stamp"] = time()
            product_dict["hash"] = self._hash()
            product_dict["score"] = self._score()
            return product_dict
        return None

    def _valid(self):
        for required in ["name", "price", "vendor_id"]:
            if getattr(self, required) is None:
                return False
        return True

    @abc.abstractmethod
    def _hash(self):
        """ Get product hash """

    @abc.abstractmethod
    def _score(self):
        """ Get product hash """