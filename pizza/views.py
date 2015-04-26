# from flask import render_template
# from pizza import pizza
#
# @pizza.route('/')
# def index():
#     return render_template('index.html')
#
# from flask import Flask, url_for
# # set the project root directory as the static folder, you can set others.
# #app = Flask(__name__, static_url_path='')
#
# @app.route('/')
# def root():
#     return url_for('static', filename='index.html')

from flask import render_template, url_for
from pizza import pizza

@pizza.route('/')
def index():
    #return url_for('static', filename='index.html')
    #return render_template(url_for('static', filename='index.html'))
    return pizza.send_static_file('index.html')