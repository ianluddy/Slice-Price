from crontab import CronTab
import time

class Collector():
    wait_between_cycles = 5

    def __init__(self, parsers, frequency, queue):
        self.parsers = parsers
        self.cron = CronTab(frequency)
        self.queue = queue

    def _collect(self):
        for parser in self.parsers:
            self.queue.put({
                "pizza": parser.get_pizzas(),
                "sides": parser.get_sides(),
                "desserts": parser.get_desserts()
            })

    def run(self):
        while True:
            self._collect()
            time.sleep(self.cron.next())