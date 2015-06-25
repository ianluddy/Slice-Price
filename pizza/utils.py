from uuid import uuid5, NAMESPACE_DNS
from lxml import html
import requests
from logging.handlers import RotatingFileHandler
import logging
import json

def read_config_file(config_file):
    with open(config_file, "r") as f:
        cfg_json = json.loads(f.read())
    return cfg_json

def make_uuid(string):
    return str(uuid5(NAMESPACE_DNS, string))

def setup_logger(app, log_file):
    logger = logging.getLogger()
    handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=2) # File handler
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:[%(module)s:%(lineno)d]:[%(threadName)s]:%(message)s')
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    ch = logging.StreamHandler() # Stream handler
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def get(url):
    page = requests.get(url)
    tree = html.fromstring(page.text)
    return tree