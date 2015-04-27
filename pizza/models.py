from pizza import app
from uuid import uuid5, NAMESPACE_DNS
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
db.create_all()

class Item():
    __tablename__ = "Item"
    uuid = db.Column(db.String(36), nullable=False, primary_key=True, index=True)
    name = db.Column(db.String(80))
    price = db.Column(db.String(80))
    vendor = db.Column(db.String(80))
    size = db.Column(db.String(80), default="standard")

class Pizza(Item, db.Model):
    __tablename__ = "Pizza"
    toppings = db.Column(db.String(80))
    diameter = db.Column(db.Integer())
    base = db.Column(db.String(80))

    def __init__(self, name=None, price=0.0, vendor=None, size=0.0, toppings=None, diameter=0.0, base=None):
        self.name = name
        self.price = float(price)
        self.vendor = vendor
        self.size = float(size)
        self.toppings = sorted([t.lower() for t in toppings])
        self.diameter = float(diameter)
        self.base = base
        self.uuid = uuid5(NAMESPACE_DNS,
                          self.name.lower() +
                          str(self.price) +
                          self.vendor.lower() +
                          str(self.size) +
                          self.toppings +
                          str(self.diameter) +
                          self.base
                          )