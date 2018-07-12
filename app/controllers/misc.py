"""Misc routes.

Any route that doesn't fit in edits.py or queries.py goes here.

"""

from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt

from ..models import db, Employee, Review, Supplier, Product, Category
from . import CustomValidator, clean_data

bcrypt = Bcrypt()

# Setup blueprint.
misc_blueprint = Blueprint(
    "misc",
    __name__,
    static_folder="../static/vue/admin/dist",
    template_folder="../static/vue/admin"
)


@misc_blueprint.route("/login/", methods=["GET", "POST"])
def login():
    """Return login page or attempt to login user."""
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        return "success"    # Auth Disable
        # Get data and clean based on schema. Validate.
        data = request.get_json()

        schema = {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "not_empty": True
                },
                "password": {
                    "type": "string",
                    "not_empty": True
                }
            },
            "required": ["email", "password"]
        }

        cleaned_data = clean_data(data, schema)

        try:
            CustomValidator(schema).validate(cleaned_data)
        except Exception as e:
            return e.message, 400

        email = cleaned_data["email"]
        password = cleaned_data["password"]

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
#@login_required
def query_employee():
    # Non-auth employee data
    return jsonify(result={"email": "username@email.com"})
    """Return logged-in employee data."""
    return jsonify(result=current_user.serialize)


@misc_blueprint.route("/update_employee_info/", methods=["POST"])
#@login_required
def update_employee_info():
    return "Updating disabled in non-auth mode", 400    # Auth Disable
    """Update employee information."""
    # Get data and clean based on schema. Validate.
    data = request.get_json()

    employee_obj = db.session.query(
        Employee
    ).filter_by(
        id=current_user.id
    ).first()

    schema = {
        "type": "object",
        "properties": {
            "account_image": {
                "type": "string"
            },
            "email": {
                "type": "integer"
            },
            "remember_me": {
                "type": "boolean"
            }
        },
        "required": ["remember_me"]
    }

    cleaned_data = clean_data(data, schema)

    try:
        CustomValidator(schema).validate(cleaned_data)
    except Exception as e:
        return e.message, 400

    # Iterate through and make modifications.
    for k, v in cleaned_data.items():
        if k != "remember_me":
            setattr(employee_obj, k, v)

    db.session.add(employee_obj)
    db.session.commit()

    # Remember me handling and relogging.
    if cleaned_data["remember_me"] is True:
        user_id = current_user.id
        this_user = db.session.query(Employee).filter_by(id=user_id).first()
        logout_user()
        login_user(this_user, remember=True)
    else:
        user_id = current_user.id
        this_user = db.session.query(Employee).filter_by(id=user_id).first()
        logout_user()
        login_user(this_user)

    return jsonify(result=employee_obj.serialize)


@misc_blueprint.route("/toggle_review/", methods=["POST"])
#@login_required
def toggle_review():
    """Toggles whether indicated review is shown."""
    review_id = request.get_json().get("id")

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
