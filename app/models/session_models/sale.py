"""Defines the Sale class.

Includes constructor, representation return, and serialization formatting.

"""

import datetime

from flask import session

from admin.app.models import db
from admin.app.models.session_models.product import ProductSession as Product


class SaleSession(db.Model):
    """Sale Class"""
    __tablename__ = "sale_session"
    real_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    price = db.Column(db.Numeric)
    timestamp_created = db.Column(db.DateTime)
    timestamp_ended = db.Column(db.DateTime)
    session_id = db.Column(db.Text)

    def __init__(
            self, product_id, price,
            timestamp_created=None, timestamp_ended=None,
            id=None, session_id=None):
        self.product_id = product_id
        self.price = price
        self.timestamp_created = (
            timestamp_created
            if timestamp_created is not None
            else datetime.datetime.utcnow()
        )
        self.timestamp_ended = timestamp_ended
        self.id = id
        self.session_id = session_id

    def __repr__(self):
        return "<Sale {}>".format(self.id)

    @property
    def serialize(self):
        """Formats for JSON return.

        This requires data from the Product model.

        """
        product_obj = db.session.query(
            Product
        ).filter_by(
            id=self.product_id,
            session_id=session.sid
        ).first()

        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": product_obj.name,
            "price": str(self.price),
            "timestamp_created": self.timestamp_created.strftime("%Y-%m-%d"),
            "timestamp_ended": (
                ""
                if self.timestamp_ended is None
                else self.timestamp_ended.strftime("%Y-%m-%d")
            )
        }
