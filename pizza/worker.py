from croniter import croniter
from datetime import datetime
import time

class Worker():
    wait_between_cycles = 5
    next_run = None

    def __init__(self, parsers, db_connection, frequency):
        self.parsers = parsers
        self.db_connection = db_connection
        self.frequency = frequency
        self._set_next_run_time()

    def _set_next_run_time(self):
        print "a"
        self.next_run = croniter(self.frequency, datetime.now()).get_next(datetime)
        print "b"

    def _ready_to_run(self):
        return self.next_run is None or self.next_run < datetime.now()

    def _persist(self, data):
        for pizza in data["pizza"]:
            self.db_connection.merge(self.db_connection.Pizza(**pizza))

    def _commit(self):
        self.db_connection.commit()
        self.db_connection.close()

    def _collect(self):
        for parser in self.parsers:
            print parser
            self._persist({
                "pizza": parser.get_pizzas(),
                "sides": parser.get_sides(),
                "desserts": parser.get_desserts()
            })
            self._commit()

    def run(self):
        while True:
            print "Waiting"
            if self._ready_to_run():
                print 1
                self._set_next_run_time()
                print 2
                self._collect()
                print 3
            time.sleep(self.wait_between_cycles)

if __name__ == "__main__":
    print croniter("* * * * *", datetime.now()).get_next(datetime)