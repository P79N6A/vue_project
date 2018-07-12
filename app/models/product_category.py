"""Defines the ProductCategory class.

Includes constructor and representation return.

"""

from admin.app.models import db


class ProductCategory(db.Model):
    """ProductCategory Class"""
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    def __init__(self, category_id, product_id):
        self.category_id = category_id
        self.product_id = product_id

    def __repr__(self):
        return "<ProductCategory {}>".format(self.id)
