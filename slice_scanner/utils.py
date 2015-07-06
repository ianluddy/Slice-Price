from flask import make_response
from uuid import uuid5, NAMESPACE_DNS
from logging.handlers import RotatingFileHandler
import logging
import json

def read_config_file(config_file):
    with open(config_file, "r") as f:
        cfg_json = json.loads(f.read())
    return cfg_json

def make_uuid(string):
    return str(uuid5(NAMESPACE_DNS, string))

def wrapped_execute(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception, e:
        logging.error("Fatal error calling %s" % str(func), exc_info=True)

def raw_response(response_string):
    response = make_response(response_string)
    response.mimetype = "text/plain"
    return response

def json_response(response):
    if type(response) in [dict, list]:
        response = json.dumps(response)
    response = make_response(response)
    response.mimetype = "application/json"
    return response

def setup_logger(app, log_file, log_level):
    logger = logging.getLogger()
    handler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=2) # File handler
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:[%(module)s:%(lineno)d]:[%(threadName)s]:%(message)s')
    handler.setFormatter(formatter)
    logger.setLevel(log_level)
    logger.addHandler(handler)
    ch = logging.StreamHandler() # Stream handler
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
