from threading import Thread
from parsers import dominos
from worker import Worker
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

# Parsers
parsers = [
    dominos.Dominos()
]

# Worker
worker = Worker(parsers, models.db, configuration["sync_freq"])
thread = Thread(target=worker.run)
thread.start()

# Views
from pizza import views

# Run
app.run()