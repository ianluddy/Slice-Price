import json
import logging

from utils import strip_dict

class Database():
    """
    Wrapper for the database layer
    """
    PAGE_SIZE = 15

    def __init__(self, db, reset_db):
        self.db = db
        if reset_db:
            self.reset_database()
        self.create_indexes()

    def create_indexes(self):
        self.db.sides.create_index("price")
        self.db.sides.create_index("score")
        self.db.sides.create_index("hash")
        self.db.pizzas.create_index("price")
        self.db.pizzas.create_index("score")
        self.db.pizzas.create_index("hash")

    def reset_database(self):
        self.db.pizzas.drop()
        self.db.meals.drop()
        self.db.desserts.drop()
        self.db.sides.drop()

    def insert_product(self, collection, product):
        print product
        json_product = product.to_dict()
        collection.remove({"hash": json_product["hash"]})
        collection.insert(json_product)

    def insert_pizza(self, pizza):
        self.insert_product(self.db.pizzas, pizza)

    def insert_side(self, side):
        self.insert_product(self.db.sides, side)

    def get_sides(self, **kwargs):
        return self.query(
            "sides",
            {
                "type": self._in(kwargs.get("type")),
            },
            sort_by=kwargs.get("sort_by"),
            sort_dir=kwargs.get("sort_dir"),
            page=kwargs.get("page")
        )

    def get_pizza(self, **kwargs):
        return self.query(
            "pizzas",
            {
                "toppings": self._all(kwargs.get("toppings")),
                "style": self._in(kwargs.get("style")),
                "base_style": self._in(kwargs.get("base_style")),
                "vendor": self._in(kwargs.get("vendor")),
                "diameter": self._in_range(kwargs.get("diameter")),
                "slices": self._in_range(kwargs.get("slices")),
                "price": self._in_range(kwargs.get("price")),
                "score": self._in_range(kwargs.get("score"))
            },
            sort_by=kwargs.get("sort_by"),
            sort_dir=kwargs.get("sort_dir"),
            page=kwargs.get("page")
        )

    def query(self, collection_name, query, sort_by=None, sort_dir=None, page=None):
        logging.info("Qry: col=%s qry=%s srt=%s:%s pg=%s" % (collection_name, query, sort_by, sort_dir, page ) )

        result = self._get_collection(collection_name).find(strip_dict(query))
        if sort_by is not None:
            sort_dir = 1 if sort_dir is None else int(sort_dir) # 1 = ascending, -1 = descending
            result = result.sort(sort_by, sort_dir)
        if page is not None:
            result = result.limit(self.PAGE_SIZE).skip(int(page) * self.PAGE_SIZE)

        return self._serialise(result)

    def all(self, collection_name):
        return self._serialise(self._get_collection(collection_name).find())

    def count(self, collection_name):
        return self._get_collection(collection_name).find().count()

    def distinct(self, collection_name, key):
        return self._get_collection(collection_name).find().distinct(key)

    def range(self, collection_name, key):
        return {
            "max": self.max(collection_name, key),
            "min": self.min(collection_name, key),
        }

    def max(self, collection_name, key):
        return self._get_collection(collection_name).find_one(sort=[(key, -1)])[key]

    def min(self, collection_name, key):
        return self._get_collection(collection_name).find_one(sort=[(key, 1)])[key]

    #### Internal ####

    @staticmethod
    def _all(arguments):
        if arguments not in [None, []]:
            return {"$all": json.loads(arguments)}

    @staticmethod
    def _gt(arguments):
        if arguments not in [None, []]:
            return {"$gt": arguments}

    @staticmethod
    def _lt(arguments):
        if arguments not in [None, []]:
            return {"$lt": arguments}

    @staticmethod
    def _in(arguments):
        if arguments is not None:
            if not arguments:
                return {"$in": arguments}
            return {"$in": json.loads(arguments)}

    @staticmethod
    def _in_range(arguments):
        if arguments is not None:
            range = json.loads(arguments)
            return {"$gte": range[0], "$lte": range[1]}

    @staticmethod
    def _serialise_document(object):
        del object["_id"] # Delete unserialisable mongo id
        return object

    def _serialise(self, cursor):
        return [self._serialise_document(obj) for obj in cursor]

    def _get_collection(self, collection_name):
        return getattr(self.db, collection_name)