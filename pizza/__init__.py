from threading import Queue
from threading import Thread
from parsers import dominos
from collector import Collector
from keeper import Keeper
from flask import Flask
from utils import *

# Config
configuration = read_config_file("D:\pizza.json")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = configuration["database"]

# Logging
setup_logger(app, configuration["log"])

# DB
from pizza import models

# Data queue
data_queue = Queue()

# Collection
parsers = [dominos.Dominos()]
collector = Collector(parsers, configuration["sync_freq"], data_queue)
thread = Thread(target=collector.run)
thread.start()

# Persistence
keeper = Keeper(data_queue)
thread = Thread(target=collector.run)
thread.start()

# Views
from pizza import views

# Run
app.run()