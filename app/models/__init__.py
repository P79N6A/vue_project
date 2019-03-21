"""Model Setup

Provides a standard place to import models from.
Also provides a standard sqlalchemy handler to interface from

"""

from flask_sqlalchemy import SQLAlchemy

# Define before other imports
db = SQLAlchemy()

# Uncomment out all before alembic model update.
# Also remove aliasing from session tables.

# Uncomment to not use session tables.

from admin.app.models.category import Category
from admin.app.models.product import Product
from admin.app.models.product_category import ProductCategory
from admin.app.models.sale import Sale
from admin.app.models.order import Order
from admin.app.models.customer import Customer
from admin.app.models.review import Review
from admin.app.models.supplier import Supplier
from admin.app.models.employee import Employee

"""

from admin.app.models.session_models.category import CategorySession as Category
from admin.app.models.session_models.product import ProductSession as Product
from admin.app.models.session_models.product_category import ProductCategorySession as ProductCategory
from admin.app.models.session_models.sale import SaleSession as Sale
from admin.app.models.session_models.order import OrderSession as Order
from admin.app.models.session_models.customer import CustomerSession as Customer
from admin.app.models.session_models.review import ReviewSession as Review
from admin.app.models.session_models.supplier import SupplierSession as Supplier
from admin.app.models.session_models.employee import EmployeeSession as Employee

"""
