"""Defines the Product class.

Includes constructor, representation return, and serialization formatting.

"""

from flask import session

from admin.app.models import db
from admin.app.models.session_models.supplier import SupplierSession as Supplier
from admin.app.models.session_models.category import CategorySession as Category
from admin.app.models.session_models.product_category import ProductCategorySession as ProductCategory


class ProductSession(db.Model):
    """Product Class"""
    __tablename__ = "product_session"
    real_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    name = db.Column(db.String(255))
    supplier_id = db.Column(db.Integer)
    units_in_stock = db.Column(db.Integer)
    unit_price = db.Column(db.Numeric)
    part_number = db.Column(db.String(255))
    image_name = db.Column(db.String(255))
    image = db.Column(db.Text)
    session_id = db.Column(db.Text)

    def __init__(
            self, name, supplier_id=None, units_in_stock=None, unit_price=None,
            part_number=None, image_name=None, image=None,
            id=None, session_id=None):
        self.name = name
        self.supplier_id = supplier_id
        self.units_in_stock = units_in_stock
        self.unit_price = unit_price
        self.part_number = part_number
        self.image_name = image_name
        self.image = image
        self.id = id
        self.session_id = session_id

    def __repr__(self):
        return "<Product {}>".format(self.name)

    @property
    def serialize(self):
        """Formats for JSON return.

        This requires data from the Supplier, Category,
        and ProductCategory models.

        """
        supplier_obj = db.session.query(
            Supplier
        ).filter_by(
            id=self.supplier_id,
            session_id=session.sid
        ).first()

        supplier_objs = db.session.query(
            Supplier
        ).filter_by(
            session_id=session.sid
        ).all()

        product_category_objs = db.session.query(
            ProductCategory
        ).filter_by(
            product_id=self.id,
            session_id=session.sid
        ).all()

        category_objs = db.session.query(
            Category
        ).filter_by(
            session_id=session.sid
        ).all()

        return {
            "id": self.id,
            "name": self.name,
            "supplier_id": self.supplier_id,
            "supplier_name": (
                None
                if supplier_obj is None
                else supplier_obj.name
            ),
            "supplier_list": [(x.id, x.name) for x in supplier_objs],
            "units_in_stock": self.units_in_stock,
            "unit_price": (
                str(self.unit_price)
                if self.unit_price is not None
                else ""
            ),
            "part_number": self.part_number,
            "image_name": (
                self.image_name.split("/")[-1]
                if self.image_name is not None
                else self.image_name
            ),
            "image": self.image,
            "category_list": [(x.id, x.name) for x in category_objs],
            "product_category_list": [
                x.category_id for x in product_category_objs
            ]
        }
