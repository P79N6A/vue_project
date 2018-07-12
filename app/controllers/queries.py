"""Query routes.

All routes that run a filter query and return a paginated result go here.
These mostly correspond to the different tabs on the front-end.

"""


import copy

from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from flask_login import login_required
from flask_bcrypt import Bcrypt

from ..models import (
    db, Product, Category, Sale,
    Order, Customer, Supplier, Review)
from . import CustomValidator, clean_data, populate_return

bcrypt = Bcrypt()

# Setup blueprint.
query_blueprint = Blueprint(
    "query",
    __name__,
    static_folder="../static/vue/admin/dist",
    template_folder="../static/vue/admin"
)

# Most queries use this schema.
# If they don't, it only requires a few modifications.
default_schema = {
    "type": "object",
    "properties": {
        "search": {
            "type": "string"
        },
        "sort_by": {
            "type": "string"
        },
        "limit": {
            "type": "integer"
        },
        "offset": {
            "type": "integer"
        }
    },
    "required": ["search", "sort_by", "limit", "offset"]
}


@query_blueprint.route("/query_parts/", methods=["POST"])
#@login_required
def query_parts():
    """Query Product objects."""
    # Get data and clean based on schema. Validate.
    data = request.get_json()
    query = data.get("query")

    schema = copy.deepcopy(default_schema)
    cleaned_data = clean_data(query, schema)
    try:
        CustomValidator(schema).validate(cleaned_data)
    except Exception as e:
        return e.message, 400

    search = cleaned_data["search"]
    sort_by = cleaned_data["sort_by"]
    limit = cleaned_data["limit"]
    offset = cleaned_data["offset"]

    # Assemble and run query.
    products = db.session.query(
        Product
    ).filter(
        or_(
            Product.name.ilike(search + "%"),
            Product.name.ilike("% " + search + "%")
        )
    )

    if sort_by == "id":
        products = products.order_by(Product.id)
    elif sort_by == "alpha":
        products = products.order_by(Product.name)

    products = products.offset(offset * limit).limit(limit + 1)

    products = products.all()

    return jsonify(result=populate_return(products, limit, offset))


@query_blueprint.route("/query_suppliers/", methods=["POST"])
#@login_required
def query_suppliers():
    """Query Supplier objects."""
    # Get data and clean based on schema. Validate.
    data = request.get_json()
    query = data.get("query")

    schema = copy.deepcopy(default_schema)
    cleaned_data = clean_data(query, schema)
    try:
        CustomValidator(schema).validate(cleaned_data)
    except Exception as e:
        return e.message, 400

    search = cleaned_data["search"]
    sort_by = cleaned_data["sort_by"]
    limit = cleaned_data["limit"]
    offset = cleaned_data["offset"]

    # Assemble and run query.
    suppliers = db.session.query(
        Supplier
    ).filter(
        or_(
            Supplier.name.ilike(search + "%"),
            Supplier.name.ilike("% " + search + "%")
        )
    )

    if sort_by == "id":
        suppliers = suppliers.order_by(Supplier.id)
    elif sort_by == "alpha":
        suppliers = suppliers.order_by(Supplier.name)

    suppliers = suppliers.offset(offset * limit).limit(limit + 1)

    suppliers = suppliers.all()

    return jsonify(result=populate_return(suppliers, limit, offset))


@query_blueprint.route("/query_transactions/", methods=["POST"])
#@login_required
def query_transactions():
    """Query Order objects."""
    # Get data and clean based on schema. Validate.
    data = request.get_json()
    query = data.get("query")

    schema = copy.deepcopy(default_schema)
    cleaned_data = clean_data(query, schema)
    try:
        CustomValidator(schema).validate(cleaned_data)
    except Exception as e:
        return e.message, 400

    search = cleaned_data["search"]
    sort_by = cleaned_data["sort_by"]
    limit = cleaned_data["limit"]
    offset = cleaned_data["offset"]

    # Assemble and run query.
    orders = db.session.query(
        Order
    ).join(
        Customer,
        Customer.id == Order.customer_id,
        isouter=True
    ).filter(
        Customer.email.ilike(search + "%")
    )

    if sort_by == "id":
        orders = orders.order_by(Order.id)
    elif sort_by == "alpha":
        orders = orders.order_by(Customer.email)
    elif sort_by == "date":
        orders = orders.order_by(Order.timestamp_created.desc())

    orders = orders.offset(offset * limit).limit(limit + 1)

    orders = orders.all()

    return jsonify(result=populate_return(orders, limit, offset))


@query_blueprint.route("/query_customers/", methods=["POST"])
#@login_required
def query_customers():
    """Query Customer objects."""
    # Get data and clean based on schema. Validate.
    data = request.get_json()
    query = data.get("query")

    schema = copy.deepcopy(default_schema)
    cleaned_data = clean_data(query, schema)
    try:
        CustomValidator(schema).validate(cleaned_data)
    except Exception as e:
        return e.message, 400

    search = cleaned_data["search"]
    sort_by = cleaned_data["sort_by"]
    limit = cleaned_data["limit"]
    offset = cleaned_data["offset"]

    # Assemble and run query.
    customers = db.session.query(
        Customer
    ).filter(
        or_(
            Customer.email.ilike(search + "%"),
            Customer.email.ilike("% " + search + "%")
        )
    )

    if sort_by == "id":
        customers = customers.order_by(Customer.id)
    elif sort_by == "alpha":
        customers = customers.order_by(Customer.email)

    customers = customers.offset(offset * limit).limit(limit + 1)

    customers = customers.all()

    return jsonify(result=populate_return(customers, limit, offset))


@query_blueprint.route("/query_sales/", methods=["POST"])
#@login_required
def query_sales():
    """Query Sales objects."""
    # Get data and clean based on schema. Validate.
    data = request.get_json()
    query = data.get("query")

    schema = copy.deepcopy(default_schema)
    # Modify schema.
    schema["properties"]["active"] = {"type": "boolean"}
    schema["required"].append("active")
    cleaned_data = clean_data(query, schema)
    try:
        CustomValidator(schema).validate(cleaned_data)
    except Exception as e:
        return e.message, 400

    search = cleaned_data["search"]
    sort_by = cleaned_data["sort_by"]
    limit = cleaned_data["limit"]
    offset = cleaned_data["offset"]
    active = cleaned_data["active"]

    # Assemble and run query.
    sales = db.session.query(
        Sale
    ).join(
        Product,
        Product.id == Sale.product_id,
        isouter=True
    ).filter(
        Product.name.ilike(search + "%")
    )

    if active is True:
        sales = sales.filter(Sale.timestamp_ended == None)

    if sort_by == "id":
        sales = sales.order_by(Sale.id)
    elif sort_by == "alpha":
        sales = sales.order_by(Product.name)
    elif sort_by == "date":
        sales = sales.order_by(Sale.timestamp_created.desc())

    sales = sales.offset(offset * limit).limit(limit + 1)

    sales = sales.all()

    return jsonify(result=populate_return(sales, limit, offset))


@query_blueprint.route("/query_categories/", methods=["POST"])
#@login_required
def query_categories():
    """Query Category objects."""
    # Get data and clean based on schema. Validate.
    data = request.get_json()
    query = data.get("query")

    schema = copy.deepcopy(default_schema)
    # Modify schema.
    schema["properties"]["active"] = {"type": "boolean"}
    schema["required"].append("active")
    cleaned_data = clean_data(query, schema)
    try:
        CustomValidator(schema).validate(cleaned_data)
    except Exception as e:
        return e.message, 400

    search = cleaned_data["search"]
    sort_by = cleaned_data["sort_by"]
    limit = cleaned_data["limit"]
    offset = cleaned_data["offset"]
    active = cleaned_data["active"]

    # Assemble and run query.
    categories = db.session.query(
        Category
    ).filter(
        Category.name.ilike(search + "%")
    )

    if active is True:
        categories = categories.filter(Category.timestamp_deleted == None)

    if sort_by == "id":
        categories = categories.order_by(Category.id)
    elif sort_by == "alpha":
        categories = categories.order_by(Category.name)

    categories = categories.offset(offset * limit).limit(limit + 1)

    categories = categories.all()

    return jsonify(result=populate_return(categories, limit, offset))


@query_blueprint.route("/query_reviews/", methods=["POST"])
#@login_required
def query_reviews():
    """Query Review objects."""
    # Get data and clean based on schema. Validate.
    data = request.get_json()
    query = data.get("query")

    schema = copy.deepcopy(default_schema)
    # Modify schema.
    schema["properties"]["product_id"] = {"type": "integer"}
    schema["properties"]["customer_id"] = {"type": "integer"}
    schema["required"] = ["sort_by", "limit", "offset"]
    cleaned_data = clean_data(query, schema)
    try:
        CustomValidator(schema).validate(cleaned_data)
    except Exception as e:
        return e.message, 400

    sort_by = cleaned_data["sort_by"]
    limit = cleaned_data["limit"]
    offset = cleaned_data["offset"]

    # Assemble and run query.
    reviews = db.session.query(
        Review
    )

    if "product_id" in cleaned_data:
        reviews = reviews.filter(
            Review.product_id == cleaned_data["product_id"]
        )
    if "customer_id" in cleaned_data:
        reviews = reviews.filter(
            Review.customer_id == cleaned_data["customer_id"]
        )

    if sort_by == "id":
        reviews = reviews.order_by(Review.id)
    elif sort_by == "date":
        reviews = reviews.order_by(Review.timestamp_created.desc())

    reviews = reviews.offset(offset * limit).limit(limit + 1)

    reviews = reviews.all()

    return jsonify(result=populate_return(reviews, limit, offset))
