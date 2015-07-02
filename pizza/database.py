import logging
from datetime import datetime, timedelta

class Database():
    """
    Wrapper for the database layer
    """
    def __init__(self, db, reset_db=False):
        self.db = db
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
            to_insert.append(json_obj)
            to_remove.append(json_obj["hash"])
        if to_remove:
            collection.remove({"hash": {"$in": to_remove}})
        if to_insert:
            collection.insert(to_insert)

    def insert_pizzas(self, pizzas):
        self.insert_batch(self.db.pizzas, pizzas)