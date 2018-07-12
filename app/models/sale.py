"""Defines the Sale class.

Includes constructor, representation return, and serialization formatting.

"""

import datetime

from admin.app.models import db
from admin.app.models.product import Product


class Sale(db.Model):
    """Sale Class"""
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    price = db.Column(db.Numeric)
    timestamp_created = db.Column(db.DateTime)
    timestamp_ended = db.Column(db.DateTime)

    def __init__(
            self, product_id, price,
            timestamp_created=None, timestamp_ended=None):
        self.product_id = product_id
        self.price = price
        self.timestamp_created = (
            timestamp_created
            if timestamp_created is not None
            else datetime.datetime.utcnow()
        )
        self.timestamp_ended = timestamp_ended

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
            id=self.product_id
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
