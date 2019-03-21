"""Edit routes.

Any route that queries a specific model and makes modifications goes here.

"""

import datetime

import bleach
from flask import Blueprint, request, jsonify
from flask_login import login_required
from flask_bcrypt import Bcrypt
from marshmallow import Schema, fields, ValidationError, pre_load, validates_schema

from ..models import (
    db, Product, Category, ProductCategory,
    Sale, Order, Customer, Supplier)
from . import CustomValidator, clean_data, process_result

bcrypt = Bcrypt()

# Setup blueprint.
edit_blueprint = Blueprint(
    "edit",
    __name__,
    static_folder="../static/vue/admin/dist",
    template_folder="../static/vue/admin"
)


# Validation Schemas
class EditPartSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    supplier_id = fields.Integer()
    units_in_stock = fields.Integer()
    unit_price = fields.Decimal()
    part_number = fields.String()
    image_name = fields.String()
    image = fields.String()
    product_categories = fields.List(fields.Integer())

    # Handle conditional required
    @validates_schema
    def conditional_required(self, data):
        if ("id" not in data or data["id"] is None) and "name" not in data:
            raise ValidationError("Name required for new items.")

    # Bleach strings
    @pre_load
    def bleach_strings(self, data):
        for k in data:
            if isinstance(data[k], str):
                data[k] = bleach.clean(data[k])


class EditSupplierSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    contact_name = fields.String()
    contact_title = fields.String()
    address = fields.String()
    city = fields.String()
    zip_code = fields.String()
    state = fields.String()
    phone = fields.String()
    contact_phone = fields.String()
    contact_email = fields.String()

    # Handle conditional required
    @validates_schema
    def conditional_required(self, data):
        if ("id" not in data or data["id"] is None) and "name" not in data:
            raise ValidationError("Name required for new items.")

    # Bleach strings
    @pre_load
    def bleach_strings(self, data):
        for k in data:
            if isinstance(data[k], str):
                data[k] = bleach.clean(data[k])


class EditTransactionsSchema(Schema):
    id = fields.Integer()
    sale_id = fields.Integer()
    customer_id = fields.Integer()

    # Handle conditional required
    @validates_schema
    def conditional_required(self, data):
        if ("id" not in data or data["id"] is None) and ("sale_id" not in data and "customer_id" not in data):
            raise ValidationError("sale_id and customer_id required for new items.")

    # Bleach strings
    @pre_load
    def bleach_strings(self, data):
        for k in data:
            if isinstance(data[k], str):
                data[k] = bleach.clean(data[k])


class EditCustomersSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    address = fields.String()
    city = fields.String()
    state = fields.String()
    zip_code = fields.String()
    phone = fields.String()
    email = fields.String()
    password_hash = fields.String()

    # Handle conditional required
    @validates_schema
    def conditional_required(self, data):
        if ("id" not in data or data["id"] is None) and ("email" not in data and "password_hash" not in data):
            raise ValidationError("email and password_hash required for new items.")

    # Bleach strings
    @pre_load
    def bleach_strings(self, data):
        for k in data:
            if isinstance(data[k], str):
                data[k] = bleach.clean(data[k])


class EditSaleSchema(Schema):
    id = fields.Integer()
    product_id = fields.Integer()
    price = fields.Decimal()
    delete = fields.Boolean()

    # Handle conditional required
    @validates_schema
    def conditional_required(self, data):
        if ("id" not in data or data["id"] is None) and ("product_id" not in data and "price" not in data):
            raise ValidationError("product_id and price required for new items.")

    # Bleach strings
    @pre_load
    def bleach_strings(self, data):
        for k in data:
            if isinstance(data[k], str):
                data[k] = bleach.clean(data[k])


class EditCategorySchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    delete = fields.Boolean()

    # Handle conditional required
    @validates_schema
    def conditional_required(self, data):
        if ("id" not in data or data["id"] is None) and "name" not in data:
            raise ValidationError("name required for new items.")

    # Bleach strings
    @pre_load
    def bleach_strings(self, data):
        for k in data:
            if isinstance(data[k], str):
                data[k] = bleach.clean(data[k])


@edit_blueprint.route("/edit_part/", methods=["POST"])
@login_required
def edit_part():
    return "Saving is disabled in demo mode", 400
    """Edit or create the Product object specified."""
    # Get data and clean based on schema. Validate.
    data = request.get_json().get("modifications")

    try:
        return_data = EditPartSchema().load(data)
        # Return silent errors
        if len(return_data.errors) > 0:
            raise ValidationError(next(iter(return_data.errors.values()))[0])
        data = return_data.data
    except ValidationError as e:
        return e.messages[0], 400

    if "id" not in data or data["id"] is None:
        # Create new object. Requires name.
        name = data["name"]

        product_obj = Product(name)
        db.session.add(product_obj)
        db.session.commit()
    else:
        product_obj = db.session.query(
            Product
        ).filter_by(
            id=data["id"]
        ).first()

    # Iterate through and make modifications.
    for k, v in data.items():
        if k != "id":
            if k not in ["product_categories"]:
                setattr(product_obj, k, v)
            else:
                #print("!")
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

    result = process_result(product_obj, ["name"])

    return jsonify(result=result)


@edit_blueprint.route("/edit_supplier/", methods=["POST"])
@login_required
def edit_supplier():
    return "Saving is disabled in demo mode", 400
    """Edit or create the Supplier object specified."""
    # Get data and clean based on schema. Validate.
    data = request.get_json().get("modifications")

    try:
        return_data = EditSupplierSchema().load(data)
        # Return silent errors
        if len(return_data.errors) > 0:
            raise ValidationError(next(iter(return_data.errors.values()))[0])
        data = return_data.data
    except ValidationError as e:
        return e.messages[0], 400

    if "id" not in data or data["id"] is None:
        # Create new object. Requires name.
        name = data["name"]

        supplier_obj = Supplier(name)
        db.session.add(supplier_obj)
        db.session.commit()
    else:
        supplier_obj = db.session.query(
            Supplier
        ).filter_by(
            id=data["id"]
        ).first()

    # Iterate through and make modifications.
    for k, v in data.items():
        if k != "id":
            setattr(supplier_obj, k, v)

    db.session.add(supplier_obj)
    db.session.commit()

    result = process_result(supplier_obj, ["name"])

    return jsonify(result=result)


@edit_blueprint.route("/edit_transactions/", methods=["POST"])
@login_required
def edit_transactions():
    return "Saving is disabled in demo mode", 400
    """Edit or create the Order object specified."""
    # Get data and clean based on schema. Validate.
    data = request.get_json().get("modifications")

    try:
        return_data = EditTransactionsSchema().load(data)
        # Return silent errors
        if len(return_data.errors) > 0:
            raise ValidationError(next(iter(return_data.errors.values()))[0])
        data = return_data.data
    except ValidationError as e:
        return e.messages[0], 400

    if "id" not in data or data["id"] is None:
        return "Creation of new orders not allowed", 400
    else:
        order_obj = db.session.query(
            Order
        ).filter_by(
            id=data["id"]
        ).first()

    # Iterate through and make modifications.
    for k, v in data.items():
        if k != "id":
            setattr(order_obj, k, v)

    db.session.add(order_obj)
    db.session.commit()

    result = process_result(order_obj, ["sale_id", "customer_id"])

    return jsonify(result=result)


@edit_blueprint.route("/edit_customer/", methods=["POST"])
@login_required
def edit_customer():
    return "Saving is disabled in demo mode", 400
    """Edit or create the Customer object specified."""
    # Get data and clean based on schema. Validate.
    data = request.get_json().get("modifications")

    try:
        return_data = EditCustomersSchema().load(data)
        # Return silent errors
        if len(return_data.errors) > 0:
            raise ValidationError(next(iter(return_data.errors.values()))[0])
        data = return_data.data
    except ValidationError as e:
        return e.messages[0], 400

    if "id" not in data or data["id"] is None:
        return "Creation of new customers not allowed", 400
    else:
        customer_obj = db.session.query(
            Customer
        ).filter_by(
            id=data["id"]
        ).first()

    # Iterate through and make modifications.
    for k, v in data.items():
        if k != "id":
            setattr(customer_obj, k, v)

    db.session.add(customer_obj)
    db.session.commit()

    result = process_result(customer_obj, ["email", "password_hash"])

    return jsonify(result=result)



@edit_blueprint.route("/edit_sale/", methods=["POST"])
@login_required
def edit_sale():
    return "Saving is disabled in demo mode", 400
    """Edit or create the Sale object specified."""
    # Get data and clean based on schema. Validate.
    data = request.get_json().get("modifications")

    try:
        return_data = EditSaleSchema().load(data)
        # Return silent errors
        if len(return_data.errors) > 0:
            raise ValidationError(next(iter(return_data.errors.values()))[0])
        data = return_data.data
    except ValidationError as e:
        return e.messages[0], 400

    if "id" not in data or data["id"] is None:
        # Create new object.
        sale_obj = Sale(data["product_id"], data["price"])
        db.session.add(sale_obj)
        db.session.commit()
    else:
        sale_obj = db.session.query(
            Sale
        ).filter_by(
            id=data["id"]
        ).first()

    # Iterate through and make modifications.
    for k, v in data.items():
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
    #print(existing_sales)

    for ind_sale in existing_sales:
        ind_sale.timestamp_ended = datetime.datetime.utcnow()
        db.session.add(ind_sale)
        db.session.commit()

    result = process_result(sale_obj, ["product_id", "price"])

    return jsonify(result=result)



@edit_blueprint.route("/edit_category/", methods=["POST"])
@login_required
def edit_category():
    return "Saving is disabled in demo mode", 400
    """Edit or create the Category object specified."""
    # Get data and clean based on schema. Validate.
    data = request.get_json().get("modifications")

    try:
        return_data = EditCategorySchema().load(data)
        # Return silent errors
        if len(return_data.errors) > 0:
            raise ValidationError(next(iter(return_data.errors.values()))[0])
        data = return_data.data
    except ValidationError as e:
        return e.messages[0], 400

    if "id" not in data or data["id"] is None:
        # Create new object. Requires name.
        name = data["name"]

        category_obj = Category(name)
        db.session.add(category_obj)
        db.session.commit()
    else:
        category_obj = db.session.query(
            Category
        ).filter_by(
            id=data["id"]
        ).first()

    # Iterate through and make modifications.
    for k, v in data.items():
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

    result = process_result(category_obj, ["name"])

    return jsonify(result=result)
