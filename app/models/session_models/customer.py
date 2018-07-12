"""Defines the Customer class.

Includes constructor, representation return, and serialization formatting.

"""

from admin.app.models import db


class CustomerSession(db.Model):
    """Customer Class"""
    __tablename__ = "customer_session"
    real_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    address = db.Column(db.Text)
    city = db.Column(db.String(255))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(255))
    password_hash = db.Column(db.Text)
    session_id = db.Column(db.Text)

    def __init__(
            self, email, password_hash, first_name=None, last_name=None,
            address=None, city=None, state=None, zip_code=None, phone=None,
            id=None, session_id=None):
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone = phone
        self.id = id
        self.session_id = session_id

    def __repr__(self):
        return "<Customer {}>".format(self.email)

    @property
    def serialize(self):
        """Formats for JSON return"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "phone": self.phone,
            "email": self.email
        }
