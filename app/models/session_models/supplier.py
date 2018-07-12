"""Defines the Supplier class.

Includes constructor, representation return, and serialization formatting.

"""

from admin.app.models import db


class SupplierSession(db.Model):
    """Supplier Class"""
    __tablename__ = "supplier_session"
    real_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    name = db.Column(db.String(255))
    contact_name = db.Column(db.String(255))
    contact_title = db.Column(db.String(255))
    address = db.Column(db.Text)
    city = db.Column(db.String(255))
    zip_code = db.Column(db.String(20))
    state = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    contact_phone = db.Column(db.String(50))
    contact_email = db.Column(db.String(255))
    session_id = db.Column(db.Text)

    def __init__(
            self, name, contact_name=None, contact_title=None,
            address=None, city=None, zip_code=None, state=None, phone=None,
            contact_phone=None, contact_email=None, id=None, session_id=None):
        self.name = name
        self.contact_name = contact_name
        self.contact_title = contact_title
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.state = state
        self.phone = phone
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        self.id = id
        self.session_id = session_id

    def __repr__(self):
        return "<Supplier {}>".format(self.name)

    @property
    def serialize(self):
        """Formats for JSON return."""
        return {
            "id": self.id,
            "name": self.name,
            "contact_name": self.contact_name,
            "contact_title": self.contact_title,
            "address": self.address,
            "city": self.city,
            "zip_code": self.zip_code,
            "state": self.state,
            "phone": self.phone,
            "contact_phone": self.contact_phone,
            "contact_email": self.contact_email
        }
