from objects.pizza import Pizza
from objects.side import Side
import logging

class Keeper():

    def __init__(self, db, queue):
        self.db = db
        self.queue = queue

    def _keep(self, product):
        if type(product) is Pizza:
            self.db.insert_pizza(product)
        elif type(product) is Side:
            self.db.insert_side(product)

    def run(self):
        logging.info("Keeper Running")
        while True:
            try:
                product = self.queue.get()
                self._keep(product)
            except Exception:
                logging.error("Error saving object [%s]" % product, exc_info=True)
            finally:
                self.queue.task_done()