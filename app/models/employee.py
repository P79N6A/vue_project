"""Defines the Employee class.

Includes constructor, representation return, and serialization formatting.
The get_id method is used in the authentication process.

"""

from flask_login import UserMixin

from admin.app.models import db


class Employee(db.Model, UserMixin):
    """Employee Class"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(250))
    account_image = db.Column(db.Text)
    is_authenticated = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)
    is_anonymous = db.Column(db.Boolean)

    def __init__(
            self, email, password_hash, is_authenticated=True,
            is_active=True, is_anonymous=False, account_image=None):
        self.email = email
        self.password_hash = password_hash
        self.is_authenticated = is_authenticated
        self.is_active = is_active
        self.is_anonymous = is_anonymous
        self.account_image = account_image

    def __repr__(self):
        return "<Employee %r>" % self.id

    def get_id(self):
        return str(self.id)

    @property
    def serialize(self):
        """Formats for JSON return"""
        return {
            "id": self.id,
            "email": self.email,
            "account_image": self.account_image
        }
