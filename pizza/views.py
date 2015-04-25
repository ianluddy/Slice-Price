from flask import render_template
from pizza import pizza

@pizza.route('/')
def index():
    return render_template('index.html')
