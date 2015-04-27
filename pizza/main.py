from utils import *
from flask import Flask

configuration = read_config_file()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = configuration["database_file"]

# Configure Logging
setup_logger(app, configuration["log_file"])