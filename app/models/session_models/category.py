"""Defines the Category class.

Includes constructor, representation return, and serialization formatting.

"""

from admin.app.models import db


class CategorySession(db.Model):
    """Category Class"""
    __tablename__ = "category_session"
    real_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    timestamp_deleted = db.Column(db.DateTime)
    session_id = db.Column(db.Text)

    def __init__(
            self, name, description=None, timestamp_deleted=None,
            id=None, session_id=None):
        self.name = name
        self.description = description
        self.timestamp_deleted = timestamp_deleted
        self.id = id
        self.session_id = session_id

    def __repr__(self):
        return "<Category {}>".format(self.name)

    @property
    def serialize(self):
        """Formats for JSON return"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "timestamp_deleted": (
                ""
                if self.timestamp_deleted is None else
                self.timestamp_deleted.strftime("%Y-%m-%d")
            )
        }
