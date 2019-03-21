import pytest

from app import create_app
import app.settings as settings
from ..models import Employee
from admin.app.models import db

@pytest.fixture(scope="session")
def test_client():
    settings_override = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": 'postgresql://{}:{}@{}:{}/{}'.format(
            settings.postgres_username,
            settings.postgres_password,
            settings.postgres_host,
            settings.postgres_port,
            "local_dev_testing"
        )
    }
    app = create_app(settings_override)
    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope="session")
def test_db(test_client):
    from ..models import (
        Product, Category, Sale, ProductCategory,
        Order, Customer, Supplier, Review
    )
    from admin.app.models import db

    # Create database and tables
    db.drop_all()
    db.create_all()

    # Insert Data
    with open("category_testing.csv", "r") as f:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cmd = "COPY category(id, name, description, timestamp_deleted) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
        cursor.copy_expert(cmd, f)
        conn.commit()

        cmd = "SELECT setval('category_id_seq', (SELECT MAX(id) FROM category)+1)"
        cursor.copy_expert(cmd, f)
        conn.commit()

    with open("customer_testing.csv", "r") as f:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cmd = "COPY customer(id, first_name, last_name, address, city, state, zip_code, phone, email, password_hash) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
        cursor.copy_expert(cmd, f)
        conn.commit()

    with open("order_testing.csv", "r") as f:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cmd = 'COPY "order"(id, sale_id, customer_id, timestamp_created) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'
        cursor.copy_expert(cmd, f)
        conn.commit()

    with open("product_category_testing.csv", "r") as f:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cmd = "COPY product_category(id, category_id, product_id) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
        cursor.copy_expert(cmd, f)
        conn.commit()

    with open("product_testing.csv", "r") as f:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cmd = "COPY product(id, name, supplier_id, units_in_stock, unit_price, part_number, image, image_name) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
        cursor.copy_expert(cmd, f)
        conn.commit()

    with open("review_testing.csv", "r") as f:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cmd = "COPY review(id, customer_id, product_id, rating, review, timestamp_created, shown) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
        cursor.copy_expert(cmd, f)
        conn.commit()

    with open("sale_testing.csv", "r") as f:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cmd = "COPY sale(id, product_id, price, timestamp_created, timestamp_ended) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
        cursor.copy_expert(cmd, f)
        conn.commit()

        cmd = "SELECT setval('sale_id_seq', (SELECT MAX(id) FROM sale)+1)"
        cursor.copy_expert(cmd, f)
        conn.commit()


    with open("supplier_testing.csv", "r") as f:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cmd = "COPY supplier(id, name, contact_name, contact_title, address, city, zip_code, state, phone, contact_phone, contact_email) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
        cursor.copy_expert(cmd, f)
        conn.commit()

    yield db
