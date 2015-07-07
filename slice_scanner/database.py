
class Database():
    """
    Wrapper for the database layer
    """
    def __init__(self, db, reset_db, vendor_info):
        self.db = db
        self.vendor_info = vendor_info
        if reset_db:
            self.reset_database()

    def reset_database(self):
        self.db.pizzas.drop()
        self.db.meals.drop()
        self.db.desserts.drop()
        self.db.sides.drop()

    #### Setters ####

    def insert_product(self, collection, product):
        print product
        json_product = product.to_dict()
        collection.remove({"hash": json_product["hash"]})
        collection.insert(json_product)

    def insert_pizza(self, pizza):
        self.insert_product(self.db.pizzas, pizza)

    def insert_side(self, side):
        self.insert_product(self.db.sides, side)

    #### Getters ####

    def get_vendors(self):
        return self.vendor_info

    def get_toppings(self):
        return self._distinct(self.db.pizzas, "toppings")

    def get_sizes(self):
        return self._distinct(self.db.pizzas, "size")

    def get_diameters(self):
        return self._distinct(self.db.pizzas, "diameter")

    def get_styles(self):
        return self._distinct(self.db.pizzas, "style")

    def get_base_styles(self):
        return self._distinct(self.db.pizzas, "base_style")

    def get_side_types(self):
        return self._distinct(self.db.sides, "type")

    def get_pizza(self, **kwargs):
        return self._serialise(self.db.pizzas.find())

    def get_sides(self, **kwargs):
        return self._serialise(self.db.sides.find())

    #### Internal ####

    def _serialise(self, cursor):
        return [self._serialise_document(obj) for obj in cursor]

    def _serialise_document(self, object):
        del object["_id"] # Delete unserialisable mongo id
        return object

    def _distinct(self, collection, key):
        return collection.find().distinct(key)