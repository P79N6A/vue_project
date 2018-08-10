"""Edit routes.

Any route that queries a specific model and makes modifications goes here.

"""

import datetime

import bleach
from flask import Blueprint, request, jsonify
from flask_login import login_required
from flask_bcrypt import Bcrypt

from ..models import (
    db, Product, Category, ProductCategory,
    Sale, Order, Customer, Supplier)
from . import CustomValidator, clean_data

bcrypt = Bcrypt()

# Setup blueprint.
edit_blueprint = Blueprint(
    "edit",
    __name__,
    static_folder="../static/vue/admin/dist",
    template_folder="../static/vue/admin"
)


@edit_blueprint.route("/edit_part/", methods=["POST"])
#@login_required
def edit_part():
    """Edit or create the Product object specified."""
    # Get data and clean based on schema. Validate.
    data = request.get_json().get("modifications")

    schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            },
            "supplier_id": {
                "type": "integer"
            },
            "units_in_stock": {
                "type": "integer"
            },
            "unit_price": {
                "type": "string"
            },
            "part_number": {
                "type": "string"
            }
        }
    }

    if "id" not in data or data["id"] is None:
        schema["required"] = ["name"]

    cleaned_data = clean_data(data, schema)

    try:
        CustomValidator(schema).validate(cleaned_data)
    except Exception as e:
        return e.message, 400

    if "id" not in cleaned_data or cleaned_data["id"] is None:
        # Create new object. Requires name.
        name = cleaned_data["name"]

        product_obj = Product(name)
        db.session.add(product_obj)
        db.session.commit()
    else:
        product_obj = db.session.query(
            Product
        ).filter_by(
            id=cleaned_data["id"]
        ).first()

    # Iterate through and make modifications.
    for k, v in cleaned_data.items():
        if k != "id":
            if k not in ["image", "product_categories"]:
                setattr(product_obj, k, v)
            elif k == "image":
                setattr(product_obj, k, bleach.clean(v["file"]))
                setattr(product_obj, "image_name", bleach.clean(v["name"]))
            else:
                # Handle product categories.
                # They are hard deleted based on the modified data passed.
                product_category_objs = db.session.query(
                    ProductCategory
                ).filter_by(
                    product_id=product_obj.id
                ).all()

                existing_ids = {x.category_id for x in product_category_objs}
                casted_v = {int(x) for x in v}
                common_ids = casted_v & existing_ids

                new_ids = casted_v - common_ids
                for ind_id in new_ids:
                    new_obj = ProductCategory(ind_id, product_obj.id)
                    db.session.add(new_obj)
                    db.session.commit()

                to_delete_ids = existing_ids - common_ids
                for ind_product_category in product_category_objs:
                    if ind_product_category.category_id in to_delete_ids:
                        db.session.delete(ind_product_category)
                        db.session.commit()

    db.session.add(product_obj)
    db.session.commit()

    return jsonify(result=product_obj.serialize)


@edit_blueprint.route("/edit_supplier/", methods=["POST"])
#@login_required
def edit_supplier():
    """Edit or create the Supplier object specified."""
    # Get data and clean based on schema. Validate.
    data = request.get_json().get("modifications")

    schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            },
            "contact_name": {
                "type": "string"
            },
            "contact_title": {
                "type": "string"
            },
            "address": {
                "type": "string"
            },
            "city": {
                "type": "string"
            },
            "zip_code": {
                "type": "string"
            },
            "state": {
                "type": "string"
            },
            "phone": {
                "type": "string"
            },
            "contact_phone": {
                "type": "string"
            },
            "contact_email": {
                "type": "string"
            }
        }
    }

    if "id" not in data or data["id"] is None:
        schema["required"] = ["name"]

    cleaned_data = clean_data(data, schema)

    try:
        CustomValidator(schema).validate(cleaned_data)
    except Exception as e:
        return e.message, 400

    if "id" not in cleaned_data or cleaned_data["id"] is None:
        # Create new object. Requires name.
        name = cleaned_data["name"]

        supplier_obj = Supplier(name)
        db.session.add(supplier_obj)
        db.session.commit()
    else:
        supplier_obj = db.session.query(
            Supplier
        ).filter_by(
            id=cleaned_data["id"]
        ).first()

    # Iterate through and make modifications.
    for k, v in cleaned_data.items():
        if k != "id":
            setattr(supplier_obj, k, v)

    db.session.add(supplier_obj)
    db.session.commit()

    return jsonify(result=supplier_obj.serialize)


@edit_blueprint.route("/edit_transactions/", methods=["POST"])
#@login_required
def edit_transactions():
    """Edit or create the Order object specified."""
    # Get data and clean based on schema. Validate.
    data = request.get_json().get("modifications")

    schema = {
        "type": "object",
        "properties": {
            "sale_id": {
                "type": "integer"
            },
            "customer_id": {
                "type": "integer"
            }
        }
    }

    if "id" not in data or data["id"] is None:
        schema["required"] = ["sale_id", "customer_id"]

    cleaned_data = clean_data(data, schema)

    try:
        CustomValidator(schema).validate(cleaned_data)
    except Exception as e:
        return e.message, 400

    if "id" not in cleaned_data or cleaned_data["id"] is None:
        return "Creation of new orders not allowed", 400
    else:
        order_obj = db.session.query(
            Order
        ).filter_by(
            id=cleaned_data["id"]
        ).first()

    # Iterate through and make modifications.
    for k, v in cleaned_data.items():
        if k != "id":
            setattr(order_obj, k, v)

    db.session.add(order_obj)
    db.session.commit()

    return jsonify(result=order_obj.serialize)


@edit_blueprint.route("/edit_customer/", methods=["POST"])
#@login_required
def edit_customer():
    """Edit or create the Customer object specified."""
    # Get data and clean based on schema. Validate.
    data = request.get_json().get("modifications")

    schema = {
        "type": "object",
        "properties": {
            "first_name": {
                "type": "string"
            },
            "last_name": {
                "type": "string"
            },
            "address": {
                "type": "string"
            },
            "city": {
                "type": "string"
            },
            "state": {
                "type": "string"
            },
            "zip_code": {
                "type": "string"
            },
            "phone": {
                "type": "string"
            },
            "email": {
                "type": "string"
            },
            "password_hash": {
                "type": "string"
            }
        }
    }

    if "id" not in data or data["id"] is None:
        schema["required"] = ["email", "password_hash"]

    cleaned_data = clean_data(data, schema)

    try:
        CustomValidator(schema).validate(cleaned_data)
    except Exception as e:
        return e.message, 400

    if "id" not in cleaned_data or cleaned_data["id"] is None:
        return "Creation of new customers not allowed", 400
    else:
        customer_obj = db.session.query(
            Customer
        ).filter_by(
            id=cleaned_data["id"]
        ).first()

    # Iterate through and make modifications.
    for k, v in cleaned_data.items():
        if k != "id":
            setattr(customer_obj, k, v)

    db.session.add(customer_obj)
    db.session.commit()

    return jsonify(result=customer_obj.serialize)


@edit_blueprint.route("/edit_sale/", methods=["POST"])
#@login_required
def edit_sale():
    """Edit or create the Sale object specified."""
    # Get data and clean based on schema. Validate.
    data = request.get_json().get("modifications")

    schema = {
        "type": "object",
        "properties": {
            "product_id": {
                "type": "integer"
            },
            "price": {
                "type": "string"
            }
        }
    }

    if "id" not in data or data["id"] is None:
        schema["required"] = ["product_id", "price"]

    cleaned_data = clean_data(data, schema)

    try:
        CustomValidator(schema).validate(cleaned_data)
    except Exception as e:
        return e.message, 400

    if "id" not in cleaned_data or cleaned_data["id"] is None:
        # Create new object.
        sale_obj = Sale(cleaned_data["product_id"], cleaned_data["price"])
        db.session.add(sale_obj)
        db.session.commit()
    else:
        sale_obj = db.session.query(
            Sale
        ).filter_by(
            id=cleaned_data["id"]
        ).first()

    # Iterate through and make modifications.
    for k, v in cleaned_data.items():
        if k != "id":
            if k != "delete":
                setattr(sale_obj, k, v)
            else:
                if v is True:
                    setattr(
                        sale_obj,
                        "timestamp_ended",
                        datetime.datetime.utcnow()
                    )

    db.session.add(sale_obj)
    db.session.commit()

    # End any existing sales on that product.
    existing_sales = db.session.query(
        Sale
    ).filter(
        Sale.product_id == sale_obj.product_id,
        Sale.id != sale_obj.id,
        Sale.timestamp_ended == None
    ).all()

    for ind_sale in existing_sales:
        ind_sale.timestamp_ended = datetime.datetime.utcnow()
        db.session.add(ind_sale)
        db.session.commit()

    return jsonify(result=sale_obj.serialize)


@edit_blueprint.route("/edit_category/", methods=["POST"])
#@login_required
def edit_category():
    """Edit or create the Category object specified."""
    # Get data and clean based on schema. Validate.
    data = request.get_json().get("modifications")

    schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            },
            "description": {
                "type": "string"
            }
        }
    }

    if "id" not in data or data["id"] is None:
        schema["required"] = ["name"]

    cleaned_data = clean_data(data, schema)

    try:
        CustomValidator(schema).validate(cleaned_data)
    except Exception as e:
        return e.message, 400

    if "id" not in cleaned_data or cleaned_data["id"] is None:
        # Create new object. Requires name.
        name = cleaned_data["name"]

        category_obj = Category(name)
        db.session.add(category_obj)
        db.session.commit()
    else:
        category_obj = db.session.query(
            Category
        ).filter_by(
            id=cleaned_data["id"]
        ).first()

    # Iterate through and make modifications.
    for k, v in cleaned_data.items():
        if k != "id":
            if k != "delete":
                setattr(category_obj, k, v)
            else:
                if v is True:
                    setattr(
                        category_obj,
                        "timestamp_deleted",
                        datetime.datetime.utcnow()
                    )
                else:
                    setattr(category_obj, "timestamp_deleted", None)

    db.session.add(category_obj)
    db.session.commit()

    return jsonify(result=category_obj.serialize)
