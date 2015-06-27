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

    def insert_pizzas(self, vendor_id, pizzas):
        self.db.pizzas.remove({"vendor_id": vendor_id})
        self.db.pizzas.insert([pizza.to_dict() for pizza in pizzas])