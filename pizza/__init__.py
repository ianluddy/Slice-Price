from flask import Flask

pizza = Flask(__name__)

from pizza import views

