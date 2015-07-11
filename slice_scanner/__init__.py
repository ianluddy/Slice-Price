from Queue import Queue
from threading import Thread
from vendors import dominos
from database import Database
from collector import Collector
from keeper import Keeper
from flask.ext.autodoc import Autodoc
from flask_pymongo import PyMongo, MongoClient
from flask import Flask
from utils import setup_logger, read_config_file

# Config
# cfg = read_config_file("D:\slice\slice.json")
cfg = read_config_file("C:\Git\pizza\slice.json")
print cfg
app = Flask(__name__, static_url_path='')
documentor = Autodoc(app)

# Logging
setup_logger(app, cfg["logging"]["file"], cfg["logging"]["level"])

# Collection
pizza_queue = Queue()
collector = Collector(cfg["collection_freq"], pizza_queue)
Thread(target=collector.run).start()

# DB
PyMongo(app)
app.config['MONGO_DBNAME'] = cfg["database"]["name"]
db_client = MongoClient(cfg["database"]["host"], cfg["database"]["port"])
db_wrapper = Database(
    db_client[cfg["database"]["name"]],
    cfg["database"]["reset"] == "true",
    collector.vendor_info()
)

# Persistence
Thread(target=Keeper(db_wrapper, pizza_queue).run).start()

# Views
from slice_scanner import views

# Run
Thread(target=app.run).start()
# app.run(host=cfg["web_server"]["host"], port=cfg["web_server"]["port"])