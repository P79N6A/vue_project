"""Defines the Order class.

Includes constructor, representation return, and serialization formatting.

"""

import datetime

from admin.app.models import db
from admin.app.models.customer import Customer
from admin.app.models.sale import Sale
from admin.app.models.product import Product


class Order(db.Model):
    """Order Class"""
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    timestamp_created = db.Column(db.DateTime)

    def __init__(self, sale_id, customer_id, timestamp_created=None):
        self.sale_id = sale_id
        self.customer_id = customer_id
        self.timestamp_created = (
            timestamp_created
            if timestamp_created is not None
            else datetime.datetime.utcnow()
        )

    def __repr__(self):
        return "<Order {}>".format(self.id)

    @property
    def serialize(self):
        """Formats for JSON return.

        This requires data from the Customer, Sale, and Product models.

        """
        customer_obj = db.session.query(
            Customer
        ).filter_by(
            id=self.customer_id
        ).first()

        sale_obj = db.session.query(
            Sale
        ).filter_by(
            id=self.sale_id
        ).first()

        product_obj = db.session.query(
            Product
        ).filter_by(
            id=sale_obj.product_id
        ).first()

        return {
            "id": self.id,
            "sale_id": self.sale_id,
            "sale_price": str(sale_obj.price),
            "sale_product": product_obj.name,
            "customer_id": self.customer_id,
            "customer_email": customer_obj.email,
            "timestamp_created": self.timestamp_created
        }
