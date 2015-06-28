import logging

class Keeper():

    def __init__(self, db, queue):
        self.db = db
        self.queue = queue

    def _keep(self, batch):

        def _insert(func, vendor, data):
            if data:
                func(vendor, data)
            else:
                logging.error("Empty data set [%s]" % str(func))

        _insert(self.db.insert_pizzas, batch["vendor"], batch["pizza"])

    def run(self):
        logging.info("Keeper Running")
        while True:
            self._keep(self.queue.get())
            self.queue.task_done()