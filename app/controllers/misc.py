"""Misc routes.

Any route that doesn't fit in edits.py or queries.py goes here.

"""

from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from marshmallow import Schema, fields, ValidationError, pre_load, validates_schema
import bleach

from ..models import db, Employee, Review, Supplier, Product, Category
from . import CustomValidator, clean_data, process_result

bcrypt = Bcrypt()

# Setup blueprint.
misc_blueprint = Blueprint(
    "misc",
    __name__,
    static_folder="../static/vue/admin/dist",
    template_folder="../static/vue/admin"
)

# Validation Schemas
class LoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)

    # Bleach strings
    @pre_load
    def bleach_strings(self, data):
        for k in data:
            if isinstance(data[k], str):
                data[k] = bleach.clean(data[k])


class EmployeeSchema(Schema):
    email = fields.String()
    account_image = fields.String()
    remember_me = fields.Boolean(required=True)

    # Bleach strings
    @pre_load
    def bleach_strings(self, data):
        for k in data:
            if isinstance(data[k], str):
                data[k] = bleach.clean(data[k])


class ReviewSchema(Schema):
    id = fields.Integer(required=True)

    # Bleach strings
    @pre_load
    def bleach_strings(self, data):
        for k in data:
            if isinstance(data[k], str):
                data[k] = bleach.clean(data[k])


@misc_blueprint.route("/login/", methods=["GET", "POST"])
def login():
    """Return login page or attempt to login user."""
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        #return "success"    # Auth Disable
        # Get data and clean based on schema. Validate.
        data = request.get_json()
        try:
            return_data = LoginSchema().load(data)
            # Return silent errors
            if len(return_data.errors) > 0:
                raise ValidationError(next(iter(return_data.errors.values()))[0])
            data = return_data.data
        except ValidationError as e:
            return e.messages[0], 400

        email = data["email"]
        password = data["password"]

        # Attempt to get user and check password.
        this_user = db.session.query(Employee).filter_by(email=email).first()
        if (this_user is None or
                bcrypt.check_password_hash(
                    this_user.password_hash, password
                ) is False):
            return "Invalid Password", 400

        # Login.
        session["email"] = email
        session["employee_id"] = this_user.id
        login_user(this_user)

        return "success"


@misc_blueprint.route("/logout/", methods=["POST"])
def logout():
    """Logout user."""
    logout_user()

    return "success"


@misc_blueprint.route("/loading/", methods=["GET"])
def loading():
    """Show loading page."""
    return render_template("loading.html")


@misc_blueprint.route("/", defaults={"path": ""}, methods=["GET"])
#@login_required
def index(path):
    """Route to index."""
    return render_template("index.html")


@misc_blueprint.route("/get_employee_info/", methods=["POST"])
@login_required
def query_employee():
    # Non-auth employee data
    #return jsonify(result={"email": "username@email.com"})
    """Return logged-in employee data."""
    processed_user = process_result(current_user, exclude_list=["password_hash", "is_authenticated", "is_active", "is_anonymous"])

    return jsonify(result=processed_user)


@misc_blueprint.route("/update_employee_info/", methods=["POST"])
@login_required
def update_employee_info():
    #return "Updating disabled in non-auth mode", 400    # Auth Disable
    """Update employee information."""
    # Get data and clean based on schema. Validate.
    data = request.get_json()

    try:
        return_data = EmployeeSchema().load(data)
        # Return silent errors
        if len(return_data.errors) > 0:
            raise ValidationError(next(iter(return_data.errors.values()))[0])
        data = return_data.data
    except ValidationError as e:
        return e.messages[0], 400

    employee_obj = db.session.query(
        Employee
    ).filter_by(
        id=current_user.id
    ).first()

    # Iterate through and make modifications.
    for k, v in data.items():
        if k != "remember_me":
            setattr(employee_obj, k, v)

    db.session.add(employee_obj)
    db.session.commit()

    # Remember me handling and relogging.
    if data["remember_me"] is True:
        user_id = current_user.id
        this_user = db.session.query(Employee).filter_by(id=user_id).first()
        logout_user()
        session["email"] = this_user.email
        session["employee_id"] = this_user.id
        login_user(this_user, remember=True)
    else:
        user_id = current_user.id
        this_user = db.session.query(Employee).filter_by(id=user_id).first()
        logout_user()
        session["email"] = this_user.email
        session["employee_id"] = this_user.id
        login_user(this_user)

    processed_user = process_result(current_user, exclude_list=["password_hash", "is_authenticated", "is_active", "is_anonymous"])

    return jsonify(result=processed_user)


@misc_blueprint.route("/toggle_review/", methods=["POST"])
@login_required
def toggle_review():
    """Toggles whether indicated review is shown."""
    data = request.get_json()

    try:
        return_data = ReviewSchema().load(data)
        # Return silent errors
        if len(return_data.errors) > 0:
            raise ValidationError(next(iter(return_data.errors.values()))[0])
        data = return_data.data
    except ValidationError as e:
        return e.messages[0], 400

    review_id = data["id"]

    review_obj = db.session.query(Review).filter_by(id=review_id).first()

    if review_obj.shown is True:
        review_obj.shown = False
    else:
        review_obj.shown = True

    db.session.add(review_obj)
    db.session.commit()

    return "success"


@misc_blueprint.route("/get_supplier_list/", methods=["POST"])
#@login_required
def get_supplier_list():
    """Returns all suppliers."""
    supplier_objs = db.session.query(Supplier).all()
    supplier_list = [(x.id, x.name) for x in supplier_objs]

    return jsonify(result=supplier_list)


@misc_blueprint.route("/get_part_list/", methods=["POST"])
#@login_required
def get_part_list():
    """Returns all parts."""
    part_objs = db.session.query(Product).all()
    part_list = [(x.id, x.name) for x in part_objs]

    return jsonify(result=part_list)


@misc_blueprint.route("/get_category_list/", methods=["POST"])
#@login_required
def get_category_list():
    """Returns all categories."""
    category_objs = db.session.query(Category).all()
    category_list = [(x.id, x.name) for x in category_objs]

    return jsonify(result=category_list)
