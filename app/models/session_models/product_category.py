"""Defines the ProductCategory class.

Includes constructor and representation return.

"""

from admin.app.models import db


class ProductCategorySession(db.Model):
    """ProductCategory Class"""
    __tablename__ = "product_category_session"
    real_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    session_id = db.Column(db.Text)

    def __init__(self, category_id, product_id, id=None, session_id=None):
        self.category_id = category_id
        self.product_id = product_id
        self.id = id
        self.session_id = session_id

    def __repr__(self):
        return "<ProductCategory {}>".format(self.id)
