from sqlalchemy import Column, String, Integer

from main import db


class Product(db.Model):
    __tablename__ = 'product_inventory'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String, unique=True)
    product_category = db.Column(db.String)
    product_name = db.Column(db.String, unique=True)
    product_description = db.Column(db.String)
    units = db.Column(db.Integer)

    def to_dictionary(self) -> dict:
        return {
            'id': '--private--',
            'p_id': self.product_id,
            'p_category': self.product_category,
            'p_name': self.product_name,
            'p_description': self.product_description,
            'p_units': self.units
        }
