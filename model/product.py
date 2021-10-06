from sqlalchemy import Column, String, Integer

from main import db


class Product(db.Model):
    __tablename__ = 'product_inventory'
    product_id = db.Column(db.Integer, primary_key=True)
    product_category = db.Column(db.String)
    product_name = db.Column(db.String)
    product_description = db.Column(db.String)
    units = db.Column(db.Integer)
