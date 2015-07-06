from slice_scanner.utils import json_response
from slice_scanner import app
from slice_scanner import documentor
from slice_scanner import db_wrapper as db

@app.route('/docs')
@documentor.doc()
def docs():
    """
    Get API documentation
    """
    return documentor.html(
        title="Slice Scanner",
        author="ianluddy@gmail.com"
    )

@app.route('/')
@documentor.doc()
def index():
    return app.send_static_file('index.html')

@app.route('/pizza')
@documentor.doc()
def pizza():
    return json_response(db.get_pizza())

@app.route('/sides')
@documentor.doc()
def sides():
    return json_response(db.get_sides())

@app.route('/vendors')
@documentor.doc()
def vendors():
    return json_response(db.get_vendors())

@app.route('/toppings')
@documentor.doc()
def toppings():
    return json_response(db.get_toppings())

@app.route('/diameters')
@documentor.doc()
def diameters():
    return json_response(db.get_diameters())

@app.route('/sizes')
@documentor.doc()
def sizes():
    return json_response(db.get_sizes())

# TODO - remove this
@app.route('/eval/<stmt>')
@documentor.doc()
def evaluate(stmt):
    return json_response(eval(stmt))