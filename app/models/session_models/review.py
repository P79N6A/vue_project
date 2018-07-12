"""Defines the Review class.

Includes constructor, representation return, and serialization formatting.

"""

import datetime

from flask import session

from admin.app.models import db
from admin.app.models.session_models.customer import CustomerSession as Customer
from admin.app.models.session_models.product import ProductSession as Product


class ReviewSession(db.Model):
    """Review Class"""
    __tablename__ = "review_session"
    real_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    rating = db.Column(db.Numeric)
    review = db.Column(db.Text)
    timestamp_created = db.Column(db.DateTime)
    shown = db.Column(db.Boolean)
    session_id = db.Column(db.Text)

    def __init__(
            self, customer_id, product_id, rating=None,
            review=None, timestamp_created=None, shown=True,
            id=None, session_id=None):
        self.customer_id = customer_id
        self.product_id = product_id
        self.rating = rating
        self.review = review
        self.timestamp_created = (
            timestamp_created
            if timestamp_created is not None
            else datetime.datetime.utcnow()
        )
        self.shown = shown
        self.id = id
        self.session_id = session_id

    def __repr__(self):
        return "<Review {}>".format(self.id)

    @property
    def serialize(self):
        """Formats for JSON return.

        This requires data from the Customer and Product models.

        """
        customer_obj = db.session.query(
            Customer
        ).filter_by(
            id=self.customer_id,
            session_id=session.sid
        ).first()

        product_obj = db.session.query(
            Product
        ).filter_by(
            id=self.product_id,
            session_id=session.sid
        ).first()

        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "customer_email": customer_obj.email,
            "product_id": self.product_id,
            "product_name": product_obj.name,
            "rating": str(self.rating),
            "review": self.review,
            "review_truncated": self.review[:100],
            "timestamp_created": self.timestamp_created,
            "shown": self.shown
        }
