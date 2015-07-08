import os
from flask import request, send_from_directory
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

# @app.route('/<path:path>')
# def static_file(path):
#     return app.send_static_file(os.path.join('static', path))
#
# @app.route('/js/<path:path>')
# def send_js(path):
#     return send_from_directory(os.path.join('static', 'js'), path)
#
# @app.route('/css/<path:path>')
# def send_css(path):
#     return send_from_directory('css', path)

### Pizza API ####

@app.route('/pizza')
@documentor.doc()
def pizza():
    return json_response(db.get_pizza(
        toppings=request.args.get("toppings"),
        style=request.args.get("style"),
        base_style=request.args.get("base_style"),
        diameter=request.args.get("diameter"),
        slices=request.args.get("slices"),
        sort_by=request.args.get("sort_by"),
        sort_dir=request.args.get("sort_dir"),
        page=request.args.get("page"),
    ))

@app.route('/pizza/toppings')
@documentor.doc()
def pizza_toppings():
    return json_response(db.distinct("pizzas", "toppings"))

@app.route('/pizza/diameters')
@documentor.doc()
def pizza_diameters():
    return json_response(db.distinct("pizzas", "diameter"))

@app.route('/pizza/styles')
@documentor.doc()
def pizza_styles():
    return json_response(db.distinct("pizzas", "style"))

@app.route('/pizza/slices')
@documentor.doc()
def pizza_slices():
    return json_response(db.distinct("pizzas", "slices"))

@app.route('/pizza/bases')
@documentor.doc()
def pizza_bases():
    return json_response(db.distinct("pizzas", "base_style"))

@app.route('/pizza/sizes')
@documentor.doc()
def pizza_sizes():
    return json_response(db.distinct("pizzas", "size"))

@app.route('/pizza/prices')
@documentor.doc()
def pizza_prices():
    return json_response(db.range("pizzas", "price"))

@app.route('/pizza/scores')
@documentor.doc()
def pizza_scores():
    return json_response(db.range("pizzas", "score"))

### Side API ####

@app.route('/sides')
@documentor.doc()
def sides():
    return json_response(db.get_sides(
        type=request.args.get("type"),
        sort_by=request.args.get("sort_by"),
        sort_dir=request.args.get("sort_dir"),
        page=request.args.get("page")
    ))

@app.route('/sides/types')
@documentor.doc()
def sides_types():
    return json_response(db.distinct("sides", "type"))

@app.route('/sides/scores')
@documentor.doc()
def sides_scores():
    return json_response(db.range("sides", "score"))

@app.route('/sides/prices')
@documentor.doc()
def sides_prices():
    return json_response(db.range("sides", "price"))

### Vendor API ####

@app.route('/vendors')
@documentor.doc()
def vendors():
    return json_response(db.vendor_info)

#### Introspector ####

# TODO - remove this
@app.route('/eval/<stmt>')
@documentor.doc()
def evaluate(stmt):
    return json_response(eval(stmt))