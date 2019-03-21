"""Query routes.

All routes that run a filter query and return a paginated result go here.
These mostly correspond to the different tabs on the front-end.

"""


import copy

from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from flask_login import login_required
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import func
from marshmallow import Schema, fields, ValidationError, pre_load, validates_schema
import time
import bleach

from ..models import (
    db, Product, Category, Sale, ProductCategory,
    Order, Customer, Supplier, Review)
from . import CustomValidator, clean_data, populate_return, process_result

bcrypt = Bcrypt()

# Setup blueprint.
query_blueprint = Blueprint(
    "query",
    __name__,
    static_folder="../static/vue/admin/dist",
    template_folder="../static/vue/admin"
)

# Validation class for queries
class QuerySchema(Schema):
    search = fields.String()
    sort_by = fields.String(required=True)
    limit = fields.Integer(required=True)
    offset = fields.Integer(required=True)
    active = fields.Boolean()
    product_id = fields.Integer()
    customer_id = fields.Integer()

    def __init__(self, extra_reqs=[]):
        self.extra_reqs = extra_reqs
        super().__init__()

    # Some extra formating
    @pre_load
    def negatives_to_zero(self, data):
        if "limit" in data:
            if type(data["limit"]) == str and "-" in data["limit"]:
                data["limit"] = "0"
            elif type(data["limit"]) == int and data["limit"] < 0:
                data["limit"] = 0
        if "offset" in data:
            if type(data["offset"]) == str and "-" in data["offset"]:
                data["offset"] = "0"
            elif type(data["offset"]) == int and data["offset"] < 0:
                data["offset"] = 0

    # Bleach strings
    @pre_load
    def bleach_strings(self, data):
        for k in data:
            if isinstance(data[k], str):
                data[k] = bleach.clean(data[k])

    # Conditional validation
    @validates_schema
    def conditional_validation(self, data):
        for required in self.extra_reqs:
            if required not in data:
                raise ValidationError("{} is required.".format(required))


@query_blueprint.route("/query_parts/", methods=["POST"])
#@login_required
def query_parts():
    """Query Product objects."""
    data = request.get_json().get("query")

    try:
        return_data = QuerySchema(["search"]).load(data)
        # Return silent errors
        if len(return_data.errors) > 0:
            raise ValidationError(next(iter(return_data.errors.values()))[0])
        data = return_data.data
    except ValidationError as e:
        return e.messages[0], 400

    search = data["search"]
    sort_by = data["sort_by"]
    limit = data["limit"]
    offset = data["offset"]

    query = db.session.query(
        Product.id,
        Product.name,
        Product.supplier_id,
        Supplier.name.label("supplier_name"),
        Product.units_in_stock,
        Product.unit_price,
        Product.part_number,
        Product.image_name,
        Product.image,
        func.array_agg(ProductCategory.category_id).label("product_category_list")
    ).join(
        Supplier,
        Supplier.id == Product.supplier_id,
        isouter=True
    ).join(
        ProductCategory,
        ProductCategory.product_id == Product.id,
        isouter=True
    ).filter(
        or_(
            Product.name.ilike(search + "%"),
            Product.name.ilike("% " + search + "%")
        )
    ).group_by(
        Product.id,
        Supplier.name
    )

    if sort_by == "id":
        query = query.order_by(Product.id)
    elif sort_by == "alpha":
        query = query.order_by(Product.name)

    query = query.offset(offset * limit).limit(limit + 1)

    query = query.all()

    query = process_result(query, ["name"])

    return jsonify(result=populate_return(query, limit, offset))


@query_blueprint.route("/query_suppliers/", methods=["POST"])
#@login_required
def query_suppliers():
    """Query Supplier objects."""
    data = request.get_json().get("query")

    try:
        return_data = QuerySchema(["search"]).load(data)
        # Return silent errors
        if len(return_data.errors) > 0:
            raise ValidationError(next(iter(return_data.errors.values()))[0])
        data = return_data.data
    except ValidationError as e:
        return e.messages[0], 400

    search = data["search"]
    sort_by = data["sort_by"]
    limit = data["limit"]
    offset = data["offset"]

    query = db.session.query(
        Supplier.id,
        Supplier.name,
        Supplier.contact_name,
        Supplier.contact_title,
        Supplier.address,
        Supplier.city,
        Supplier.zip_code,
        Supplier.state,
        Supplier.phone,
        Supplier.contact_phone,
        Supplier.contact_email
    ).filter(
        or_(
            Supplier.name.ilike(search + "%"),
            Supplier.name.ilike("% " + search + "%")
        )
    )

    if sort_by == "id":
        query = query.order_by(Supplier.id)
    elif sort_by == "alpha":
        query = query.order_by(Supplier.name)

    query = query.offset(offset * limit).limit(limit + 1)

    query = query.all()

    query = process_result(query, ["name"])

    return jsonify(result=populate_return(query, limit, offset))


@query_blueprint.route("/query_transactions/", methods=["POST"])
#@login_required
def query_transactions():
    """Query Order objects."""
    data = request.get_json().get("query")

    try:
        return_data = QuerySchema(["search"]).load(data)
        # Return silent errors
        if len(return_data.errors) > 0:
            raise ValidationError(next(iter(return_data.errors.values()))[0])
        data = return_data.data
    except ValidationError as e:
        return e.messages[0], 400

    search = data["search"]
    sort_by = data["sort_by"]
    limit = data["limit"]
    offset = data["offset"]

    query = db.session.query(
        Order.id,
        Order.sale_id,
        Sale.price,
        Product.name,
        Order.customer_id,
        Customer.email,
        Order.timestamp_created
    ).join(
        Customer,
        Customer.id == Order.customer_id,
        isouter=True
    ).join(
        Sale,
        Sale.id == Order.sale_id,
        isouter=True
    ).join(
        Product,
        Product.id == Sale.product_id,
        isouter=True
    ).filter(
        Customer.email.ilike(search + "%")
    )

    if sort_by == "id":
        query = query.order_by(Order.id)
    elif sort_by == "alpha":
        query = query.order_by(Customer.email)
    elif sort_by == "date":
        orders = query.order_by(Order.timestamp_created.desc())

    query = query.offset(offset * limit).limit(limit + 1)

    query = query.all()

    query = process_result(query, ["sale_id", "customer_id"])

    return jsonify(result=populate_return(query, limit, offset))


@query_blueprint.route("/query_customers/", methods=["POST"])
#@login_required
def query_customers():
    """Query Customer objects."""
    data = request.get_json().get("query")

    try:
        return_data = QuerySchema(["search"]).load(data)
        # Return silent errors
        if len(return_data.errors) > 0:
            raise ValidationError(next(iter(return_data.errors.values()))[0])
        data = return_data.data
    except ValidationError as e:
        return e.messages[0], 400

    search = data["search"]
    sort_by = data["sort_by"]
    limit = data["limit"]
    offset = data["offset"]

    query = db.session.query(
        Customer.id,
        Customer.first_name,
        Customer.last_name,
        Customer.address,
        Customer.city,
        Customer.state,
        Customer.zip_code,
        Customer.phone,
        Customer.email
    ).filter(
        Customer.email.ilike(search + "%")
    )

    if sort_by == "id":
        query = query.order_by(Customer.id)
    elif sort_by == "alpha":
        query = query.order_by(Customer.email)

    query = query.offset(offset * limit).limit(limit + 1)

    query = query.all()

    query = process_result(query, ["email", "password_hash"])

    return jsonify(result=populate_return(query, limit, offset))


@query_blueprint.route("/query_sales/", methods=["POST"])
#@login_required
def query_sales():
    """Query Sales objects."""
    data = request.get_json().get("query")

    try:
        return_data = QuerySchema(["search", "active"]).load(data)
        # Return silent errors
        if len(return_data.errors) > 0:
            raise ValidationError(next(iter(return_data.errors.values()))[0])
        data = return_data.data
    except ValidationError as e:
        return e.messages[0], 400

    search = data["search"]
    sort_by = data["sort_by"]
    limit = data["limit"]
    offset = data["offset"]
    active = data["active"]

    query = db.session.query(
        Sale.id,
        Sale.product_id,
        Product.name,
        Sale.price,
        Sale.timestamp_created,
        Sale.timestamp_ended
    ).join(
        Product,
        Sale.product_id == Product.id,
        isouter=True
    ).filter(
        Product.name.ilike(search + "%")
    )

    if active is True:
        query = query.filter(Sale.timestamp_ended == None)

    if sort_by == "id":
        query = query.order_by(Sale.id)
    elif sort_by == "alpha":
        query = query.order_by(Product.name)
    elif sort_by == "date":
        query = query.order_by(Sale.timestamp_created.desc())

    query = query.offset(offset * limit).limit(limit + 1)

    query = query.all()

    query = process_result(query, ["product_id", "price"])

    return jsonify(result=populate_return(query, limit, offset))


@query_blueprint.route("/query_categories/", methods=["POST"])
#@login_required
def query_categories():
    """Query Sales objects."""
    data = request.get_json().get("query")

    try:
        return_data = QuerySchema(["search", "active"]).load(data)
        # Return silent errors
        if len(return_data.errors) > 0:
            raise ValidationError(next(iter(return_data.errors.values()))[0])
        data = return_data.data
    except ValidationError as e:
        return e.messages[0], 400

    search = data["search"]
    sort_by = data["sort_by"]
    limit = data["limit"]
    offset = data["offset"]
    active = data["active"]

    query = db.session.query(
        Category.id,
        Category.name,
        Category.description,
        Category.timestamp_deleted
    ).filter(
        Category.name.ilike(search + "%")
    )

    if active is True:
        query = query.filter(Category.timestamp_deleted == None)

    if sort_by == "id":
        query = query.order_by(Category.id)
    elif sort_by == "alpha":
        query = query.order_by(Category.name)

    query = query.offset(offset * limit).limit(limit + 1)

    query = query.all()

    query = process_result(query, ["name"])

    return jsonify(result=populate_return(query, limit, offset))


@query_blueprint.route("/query_reviews/", methods=["POST"])
#@login_required
def query_reviews():
    """Query Sales objects."""
    data = request.get_json().get("query")

    try:
        return_data = QuerySchema().load(data)
        # Return silent errors
        if len(return_data.errors) > 0:
            raise ValidationError(next(iter(return_data.errors.values()))[0])
        data = return_data.data
    except ValidationError as e:
        return e.messages[0], 400

    sort_by = data["sort_by"]
    limit = data["limit"]
    offset = data["offset"]

    query = db.session.query(
        Review.id,
        Review.customer_id,
        Customer.email.label("customer_email"),
        Review.product_id,
        Product.name.label("product_name"),
        Review.rating,
        Review.review,
        Review.timestamp_created,
        Review.shown
    ).join(
        Customer,
        Review.customer_id == Customer.id,
        isouter=True
    ).join(
        Product,
        Review.product_id == Product.id,
        isouter=True
    )

    if "product_id" in data:
        query = query.filter(
            Review.product_id == data["product_id"]
        )
    if "customer_id" in data:
        query = query.filter(
            Review.customer_id == data["customer_id"]
        )

    if sort_by == "id":
        query = query.order_by(Review.id)
    elif sort_by == "date":
        query = query.order_by(Review.timestamp_created.desc())

    query = query.offset(offset * limit).limit(limit + 1)

    query = query.all()

    query = process_result(query, ["customer_id", "product_id"])

    return jsonify(result=populate_return(query, limit, offset))
