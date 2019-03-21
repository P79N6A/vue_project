import json
import decimal
import base64

import pprint

from . import auth_handler
from ..models import (
    Product, Category, Sale, ProductCategory,
    Order, Customer, Supplier, Review
)
from admin.app.models import db

def edit_general(test_client, model, route, modifications_dict, expected_status):
    test_model = db.session.query(model).order_by(model.id).first()

    attribute_check = []
    attribute_check_value = []

    for k, v in modifications_dict.items():
        attribute_check.append(k)
        attribute_check_value.append(v)

    modifications_dict["id"] = test_model.id

    response = test_client.post(
        route,
        json={
            "modifications": modifications_dict
        }
    )
    assert response.status_code == expected_status

    updated_test_model = db.session.query(model).filter_by(id=test_model.id).first()

    assert updated_test_model != None

    if expected_status == 200:
        for attrib, attrib_value in zip(attribute_check, attribute_check_value):
            cast_type = type(getattr(test_model, attrib))
            if cast_type != type(None):
                assert getattr(test_model, attrib) != cast_type(getattr(updated_test_model, attrib))
                assert getattr(updated_test_model, attrib) == cast_type(attrib_value)
    else:
        for attrib, attrib_value in zip(attribute_check, attribute_check_value):
            cast_type = type(getattr(test_model, attrib))
            if cast_type != type(None):
                assert getattr(test_model, attrib) == cast_type(getattr(updated_test_model, attrib))
                try:
                    assert getattr(updated_test_model, attrib) != cast_type(attrib_value)
                except: #ValueError: # ! Need invalid literal decimal fix, too
                    pass

def create_general(test_client, model, route, modifications_dict, expected_status):
    test_ids = [x.id for x in db.session.query(model).all()]

    attribute_check = []
    attribute_check_value = []

    for k, v in modifications_dict.items():
        attribute_check.append(k)
        attribute_check_value.append(v)

    response = test_client.post(
        route,
        json={
            "modifications": modifications_dict
        }
    )
    assert response.status_code == expected_status

    if expected_status == 200:
        new_obj_id = json.loads(response.data.decode("utf-8"))["result"][0]["id"]["value"]

        assert new_obj_id not in test_ids

        new_obj = db.session.query(model).filter_by(id=new_obj_id).first()
        assert new_obj != None

        for attrib, attrib_value in zip(attribute_check, attribute_check_value):
            cast_type = type(getattr(new_obj, attrib))
            assert getattr(new_obj, attrib) == cast_type(attrib_value)

class TestParts():
    def test_edit_existing_part(self, test_client, test_db):
        with auth_handler(test_client):
            edit_general(test_client, Product, "/edit_part/", {"name": "TEST"}, 200)
            edit_general(test_client, Product, "/edit_part/", {"supplier_id": 5}, 200)
            edit_general(test_client, Product, "/edit_part/", {"units_in_stock": 7}, 200)
            edit_general(test_client, Product, "/edit_part/", {"unit_price": "23.15"}, 200)
            edit_general(test_client, Product, "/edit_part/", {"part_number": "DFKFO65"}, 200)
            edit_general(test_client, Product, "/edit_part/", {"image_name": "test_name"}, 200)
            with open("test_image.png", "rb") as f:
                edit_general(test_client, Product, "/edit_part/", {"image": base64.b64encode(f.read()).decode()}, 200)

    def test_create_part(self, test_client, test_db):
        with auth_handler(test_client):
            create_general(test_client, Product, "/edit_part/", {"name": "TEST"}, 200)
            with open("test_image.png", "rb") as f:
                create_general(
                    test_client,
                    Product,
                    "/edit_part/",
                    {
                        "name": "TEST_2",
                        "supplier_id": 8,
                        "units_in_stock": 3,
                        "unit_price": "22.55",
                        "part_number": "3K5K7I4TR",
                        "image_name": "test_name_2",
                        "image": base64.b64encode(f.read()).decode()
                    },
                    200
                )

    def test_product_category(self, test_client, test_db):
        with auth_handler(test_client):
            existing_part = db.session.query(Product).first()
            assert existing_part != None

            response = test_client.post(
                "/edit_part/",
                json={
                    "modifications": {
                        "id": existing_part.id,
                        "product_categories": ["1", "2"]
                    }
                }
            )
            assert response.status_code == 200

            starting_categories = db.session.query(ProductCategory).filter_by(product_id=existing_part.id).all()

            response = test_client.post(
                "/edit_part/",
                json={
                    "modifications": {
                        "id": existing_part.id,
                        "product_categories": ["2", "3", "5"]
                    }
                }
            )
            assert response.status_code == 200

            ending_categories = db.session.query(ProductCategory).filter_by(product_id=existing_part.id).all()

            assert starting_categories != ending_categories
            assert "1" not in [str(x.category_id) for x in ending_categories]
            assert [str(x.category_id) for x in ending_categories] == ["2", "3", "5"]

    def test_edit_existing_part_fail(self, test_client, test_db):
        with auth_handler(test_client):
            edit_general(test_client, Product, "/edit_part/", {"name": 999}, 400)
            edit_general(test_client, Product, "/edit_part/", {"supplier_id": "test"}, 400)
            edit_general(test_client, Product, "/edit_part/", {"units_in_stock": "test"}, 400)
            edit_general(test_client, Product, "/edit_part/", {"unit_price": "test"}, 400)
            edit_general(test_client, Product, "/edit_part/", {"part_number": 5}, 400)
            edit_general(test_client, Product, "/edit_part/", {"image_name": 5}, 400)
            edit_general(test_client, Product, "/edit_part/", {"image": 5}, 400)

    def test_create_part_fail(self, test_client, test_db):
        with auth_handler(test_client):
            create_general(test_client, Product, "/edit_part/", {}, 400)
            create_general(test_client, Product, "/edit_part/", {"unit_price": "test"}, 400)
            with open("test_image.png", "rb") as f:
                create_general(
                    test_client,
                    Product,
                    "/edit_part/",
                    {
                        "name": "TEST_2",
                        "supplier_id": 8,
                        "units_in_stock": "test",
                        "unit_price": "22.55",
                        "part_number": "3K5K7I4TR",
                        "image_name": "test_name_2",
                        "image": base64.b64encode(f.read()).decode()
                    },
                    400
                )

class TestSuppliers():
    def test_edit_existing_supplier(self, test_client, test_db):
        with auth_handler(test_client):
            edit_general(test_client, Supplier, "/edit_supplier/", {"name": "TEST"}, 200)
            edit_general(test_client, Supplier, "/edit_supplier/", {"contact_name": "Bob Test"}, 200)
            edit_general(test_client, Supplier, "/edit_supplier/", {"contact_title": "Tester"}, 200)
            edit_general(test_client, Supplier, "/edit_supplier/", {"address": "123 Test Str."}, 200)
            edit_general(test_client, Supplier, "/edit_supplier/", {"city": "Testing"}, 200)
            edit_general(test_client, Supplier, "/edit_supplier/", {"zip_code": "00000"}, 200)
            edit_general(test_client, Supplier, "/edit_supplier/", {"state": "ZZ"}, 200)
            edit_general(test_client, Supplier, "/edit_supplier/", {"phone": "2222222222"}, 200)
            edit_general(test_client, Supplier, "/edit_supplier/", {"contact_phone": "1111111111"}, 200)
            edit_general(test_client, Supplier, "/edit_supplier/", {"contact_email": "testing@test.com"}, 200)

    def test_create_supplier(self, test_client, test_db):
        with auth_handler(test_client):
            create_general(test_client, Supplier, "/edit_supplier/", {"name": "TEST"}, 200)
            create_general(
                test_client,
                Supplier,
                "/edit_supplier/",
                {
                    "name": "TEST2",
                    "contact_name": "Bob Test2",
                    "contact_title": "Tester2",
                    "address": "123 Test Str. Apt. 2",
                    "city": "Testing2",
                    "zip_code": "00002",
                    "state": "ZA",
                    "phone": "2222222223",
                    "contact_phone": "1111111112",
                    "contact_email": "testing2@test.com"
                },
                200
            )

    def test_edit_existing_supplier_fail(self, test_client, test_db):
        with auth_handler(test_client):
            edit_general(test_client, Supplier, "/edit_supplier/", {"name": 999}, 400)
            edit_general(test_client, Supplier, "/edit_supplier/", {"contact_name": 5}, 400)
            edit_general(test_client, Supplier, "/edit_supplier/", {"contact_title": 5}, 400)
            edit_general(test_client, Supplier, "/edit_supplier/", {"address": 5}, 400)
            edit_general(test_client, Supplier, "/edit_supplier/", {"city": 5}, 400)
            edit_general(test_client, Supplier, "/edit_supplier/", {"zip_code": 5}, 400)
            edit_general(test_client, Supplier, "/edit_supplier/", {"state": 5}, 400)
            edit_general(test_client, Supplier, "/edit_supplier/", {"phone": 5}, 400)
            edit_general(test_client, Supplier, "/edit_supplier/", {"contact_phone": 5}, 400)
            edit_general(test_client, Supplier, "/edit_supplier/", {"contact_email": 5}, 400)

    def test_create_supplier_fail(self, test_client, test_db):
        with auth_handler(test_client):
            create_general(test_client, Supplier, "/edit_supplier/", {}, 400)
            create_general(
                test_client,
                Supplier,
                "/edit_supplier/",
                {
                    "name": "TEST2",
                    "contact_name": "Bob Test2",
                    "contact_title": "Tester2",
                    "address": "123 Test Str. Apt. 2",
                    "city": "Testing2",
                    "zip_code": "00002",
                    "state": "ZA",
                    "phone": "2222222223",
                    "contact_phone": "1111111112",
                    "contact_email": 5
                },
                400
            )


class TestTransactions():
    def test_edit_existing_transaction(self, test_client, test_db):
        with auth_handler(test_client):
            edit_general(test_client, Order, "/edit_transactions/", {"sale_id": 999}, 200)
            edit_general(test_client, Order, "/edit_transactions/", {"customer_id": 999}, 200)

    def test_edit_existing_transaction_fail(self, test_client, test_db):
        with auth_handler(test_client):
            edit_general(test_client, Order, "/edit_transactions/", {"sale_id": "test"}, 400)
            edit_general(test_client, Order, "/edit_transactions/", {"customer_id": "test"}, 400)

    
class TestCustomers():
    def test_edit_existing_customer(self, test_client, test_db):
        with auth_handler(test_client):
            edit_general(test_client, Customer, "/edit_customer/", {"first_name": "Test"}, 200)
            edit_general(test_client, Customer, "/edit_customer/", {"last_name": "Test"}, 200)
            edit_general(test_client, Customer, "/edit_customer/", {"address": "123 Test Str."}, 200)
            edit_general(test_client, Customer, "/edit_customer/", {"city": "Testing"}, 200)
            edit_general(test_client, Customer, "/edit_customer/", {"state": "ZZ"}, 200)
            edit_general(test_client, Customer, "/edit_customer/", {"zip_code": "00000"}, 200)
            edit_general(test_client, Customer, "/edit_customer/", {"phone": "2222222222"}, 200)
            edit_general(test_client, Customer, "/edit_customer/", {"email": "testing@test.com"}, 200)
            edit_general(test_client, Customer, "/edit_customer/", {"password_hash": "TestTestTestTest"}, 200)

    def test_edit_existing_customer_fail(self, test_client, test_db):
        with auth_handler(test_client):
            edit_general(test_client, Customer, "/edit_customer/", {"first_name": 5}, 400)
            edit_general(test_client, Customer, "/edit_customer/", {"last_name": 5}, 400)
            edit_general(test_client, Customer, "/edit_customer/", {"address": 5}, 400)
            edit_general(test_client, Customer, "/edit_customer/", {"city": 5}, 400)
            edit_general(test_client, Customer, "/edit_customer/", {"state": 5}, 400)
            edit_general(test_client, Customer, "/edit_customer/", {"zip_code": 5}, 400)
            edit_general(test_client, Customer, "/edit_customer/", {"phone": 5}, 400)
            edit_general(test_client, Customer, "/edit_customer/", {"email": 5}, 400)
            edit_general(test_client, Customer, "/edit_customer/", {"password_hash": 5}, 400)


class TestSales():
    def test_edit_existing_sale(self, test_client, test_db):
        with auth_handler(test_client):
            edit_general(test_client, Sale, "/edit_sale/", {"product_id": 999}, 200)
            edit_general(test_client, Sale, "/edit_sale/", {"price": "23.15"}, 200)

    def test_create_sale(self, test_client, test_db):
        with auth_handler(test_client):
            create_general(
                test_client,
                Sale,
                "/edit_sale/",
                {
                    "product_id": 9999,
                    "price": "1111.96"
                },
                200
            )

    def test_delete_sale(self, test_client, test_db):
        with auth_handler(test_client):
            existing_sale = db.session.query(Sale).filter_by(timestamp_ended=None).first()
            assert existing_sale != None
            assert existing_sale.timestamp_ended == None

            response = test_client.post(
                "/edit_sale/",
                json={
                    "modifications": {
                        "id": existing_sale.id,
                        "delete": True
                    }
                }
            )
            assert response.status_code == 200

            existing_sale_requery = db.session.query(Sale).filter_by(id=existing_sale.id).first()
            assert existing_sale_requery != None
            assert existing_sale_requery.timestamp_ended != None

    def test_existing_sale_ended(self, test_client, test_db):
        with auth_handler(test_client):
            existing_sale = db.session.query(Sale).filter_by(timestamp_ended=None).first()
            assert existing_sale != None
            assert existing_sale.timestamp_ended == None

            response = test_client.post(
                "/edit_sale/",
                json={
                    "modifications": {
                        "product_id": existing_sale.product_id,
                        "price": "1111.96"
                    }
                }
            )
            assert response.status_code == 200

            existing_sale_requery = db.session.query(Sale).filter_by(id=existing_sale.id).first()
            assert existing_sale_requery != None
            assert existing_sale_requery.timestamp_ended != None

    def test_edit_existing_sale_fail(self, test_client, test_db):
        with auth_handler(test_client):
            edit_general(test_client, Sale, "/edit_sale/", {"product_id": "test"}, 400)
            edit_general(test_client, Sale, "/edit_sale/", {"price": "test"}, 400)

    def test_create_sale_fail(self, test_client, test_db):
        with auth_handler(test_client):
            create_general(test_client, Sale, "/edit_sale/", {}, 400)
            create_general(
                test_client,
                Sale,
                "/edit_sale/",
                {
                    "product_id": 9999,
                    "price": "test"
                },
                400
            )


class TestCategories():
    def test_edit_existing_category(self, test_client, test_db):
        with auth_handler(test_client):
            edit_general(test_client, Category, "/edit_category/", {"name": "TEST"}, 200)
            edit_general(test_client, Category, "/edit_category/", {"description": "Test Test Test Test"}, 200)

    def test_create_category(self, test_client, test_db):
        with auth_handler(test_client):
            create_general(test_client, Category, "/edit_category", {"name": "TEST2"}, 200)
            create_general(
                test_client,
                Category,
                "/edit_category/",
                {
                    "name": "TEST3",
                    "description": "Test Test"
                },
                200
            )

    def test_delete_category(self, test_client, test_db):
        with auth_handler(test_client):
            existing_category = db.session.query(Category).filter_by(timestamp_deleted=None).first()
            assert existing_category != None
            assert existing_category.timestamp_deleted == None

            response = test_client.post(
                "/edit_category/",
                json={
                    "modifications": {
                        "id": existing_category.id,
                        "delete": True
                    }
                }
            )
            assert response.status_code == 200

            existing_category_requery = db.session.query(Category).filter_by(id=existing_category.id).first()
            assert existing_category_requery != None
            assert existing_category_requery.timestamp_deleted != None

    def test_edit_existing_category_fail(self, test_client, test_db):
        with auth_handler(test_client):
            edit_general(test_client, Category, "/edit_category/", {"name": 5}, 400)
            edit_general(test_client, Category, "/edit_category/", {"description": 5}, 400)

    def test_create_category_fail(self, test_client, test_db):
        with auth_handler(test_client):
            create_general(test_client, Category, "/edit_category", {}, 400)
            create_general(
                test_client,
                Category,
                "/edit_category/",
                {
                    "name": "TEST3",
                    "description": 5
                },
                400
            )
