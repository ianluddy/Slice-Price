import logging

class Keeper():

    def __init__(self, db, queue):
        self.db = db
        self.queue = queue

    def _keep(self, batch):
        self.db.insert_pizzas(batch["pizza"])
        self.db.insert_sides(batch["sides"])

    def run(self):
        logging.info("Keeper Running")
        while True:
            self._keep(self.queue.get())
            self.queue.task_done()