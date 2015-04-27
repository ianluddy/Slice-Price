from logging.handlers import RotatingFileHandler
from devices import emulator
import os
import datetime
import logging
import json

def read_config_file(config_file):
    with open(config_file, "r") as f:
        cfg_json = json.loads(f.read())
    return cfg_json

def setup_logger(app, log_file):
    handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)
