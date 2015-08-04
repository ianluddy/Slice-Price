import argparse
from Queue import Queue
from threading import Thread
from vendors import dominos
from database import Database
from collector import Collector
from cleaner import Cleaner
from keeper import Keeper
from flask.ext.autodoc import Autodoc
from flask_pymongo import MongoClient
from flask import Flask
from utils import setup_logger, read_config_file

# Argument parser
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-c") # Config arg
args = arg_parser.parse_args()

# Config
cfg = read_config_file(args.c)

# Logging
setup_logger(cfg["logging"]["file"], cfg["logging"]["level"])

# DB
db_client = MongoClient(cfg["database"]["host"], cfg["database"]["port"])
db_wrapper = Database(db_client[cfg["database"]["name"]])

# Cleaner
if cfg["cleaner"]["enabled"]:
    Thread(target=Cleaner(cfg["cleaner"]["frequency"], cfg["cleaner"]["data_expiry_hours"], db_wrapper).run).start()

# Scraper
if cfg["scraper"]["enabled"]:
    # Collection
    pizza_queue = Queue()
    Thread(target=Collector(cfg["scraper"]["frequency"], cfg["scraper"]["web_driver"], pizza_queue).run).start()

    # Persistence
    Thread(target=Keeper(db_wrapper, pizza_queue).run).start()

# Web Server
if cfg["web_server"]["enabled"]:
    # Create Server
    app = Flask(__name__, static_url_path='')
    documentor = Autodoc(app)

    # Run Server
    from slice_scanner import views
    Thread(target=app.run, args=(cfg["web_server"]["host"], cfg["web_server"]["port"]) ).start()