
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

    def insert_batch(self, collection, data):
        to_insert = []
        to_remove = []
        for obj in data:
            json_obj = obj.to_dict()
            if json_obj: # Return None if incomplete object
                to_insert.append(json_obj)
                to_remove.append(json_obj["hash"])
        if to_remove:
            collection.remove({"hash": {"$in": to_remove}})
        if to_insert:
            collection.insert(to_insert)

    def insert_pizzas(self, pizzas):
        self.insert_batch(self.db.pizzas, pizzas)

    def insert_sides(self, sides):
        self.insert_batch(self.db.sides, sides)

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