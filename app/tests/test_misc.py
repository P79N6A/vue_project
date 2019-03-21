import base64
import json

from flask import session
from flask_login import current_user
import bleach

from . import auth_handler
from ..models import Employee, Review
from admin.app.models import db

class TestPages():
    def test_loading(self, test_client, test_db):
        response = test_client.get(
            "/loading/"
        )
        assert response.status_code == 200
        assert b"Loading..." in response.data

    def test_index(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.get(
                "/"
            )
            assert response.status_code == 200
            assert b'<div id="app">' in response.data

    def test_login_get(self, test_client, test_db):
        response = test_client.get(
            "/login/"
        )
        assert response.status_code == 200
        assert b'<div id="app">' in response.data

    def test_page_not_found(self, test_client, test_db):
        response = test_client.get(
            "/JKLSDFJKLSDFJKL/"
        )
        assert response.status_code == 302

        response = test_client.get(
            "/JKLSDFJKLSDFJKL/",
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'<div id="app">' in response.data

class TestAuth():
    def test_auth_success(self, test_client, test_db):
        with auth_handler(test_client):
            with test_client.session_transaction() as sess:
                assert sess["email"] == "tester"

        with test_client.session_transaction() as sess:
            assert "email" not in sess

    def test_auth_fail(self, test_client, test_db):
        with auth_handler(test_client, password="test", expected_status=400):
            with test_client.session_transaction() as sess:
                assert "email" not in sess

class TestEmployeeInfo():
    def test_get_employee_info_auth(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/get_employee_info/"
            )
            assert response.status_code == 200

    def test_get_employee_info_nonauth(self, test_client, test_db):
        response = test_client.post(
            "/get_employee_info/"
        )
        assert response.status_code == 302

        response = test_client.post(
            "/get_employee_info/",
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'<div id="app">' in response.data

    def test_update_employee_info_success(self, test_client, test_db):
        with auth_handler(test_client):
            with test_client.session_transaction() as sess:
                this_user = db.session.query(Employee).filter_by(id=sess["employee_id"]).first()
                assert this_user != None
                assert this_user.email == "tester"
                assert sess["email"] == "tester"
            
            response = test_client.post(
                "/update_employee_info/",
                json={
                    "email": "tester_2",
                    "remember_me": False
                }
            )
            assert response.status_code == 200

            with test_client.session_transaction() as sess:
                this_user = db.session.query(Employee).filter_by(id=sess["employee_id"]).first()
                assert this_user != None
                assert this_user.email == "tester_2"
                assert sess["email"] == "tester_2"

            with open("test_image.png", "rb") as f:
                image_string = base64.b64encode(f.read()).decode()
                response = test_client.post(
                    "/update_employee_info/",
                    json={
                        "account_image": image_string,
                        "remember_me": False
                    }
                )
                assert response.status_code == 200

                with test_client.session_transaction() as sess:
                    this_user = db.session.query(Employee).filter_by(id=sess["employee_id"]).first()
                    assert this_user != None
                    assert this_user.account_image == image_string

    def test_update_employee_info_fail(self, test_client, test_db):
        # Non-Auth Tests
        response = test_client.post(
            "/update_employee_info/",
            json={
                "email": "tester_2",
                "remember_me": False
            }
        )
        assert response.status_code == 302

        response = test_client.post(
            "/update_employee_info/",
            json={
                "email": "tester_2",
                "remember_me": False
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'<div id="app">' in response.data

        with auth_handler(test_client):
            # No remember_me test
            response = test_client.post(
                "/update_employee_info/",
                json={
                    "email": "tester_2"
                }
            )
            assert response.status_code == 400

            # Invalid type tests
            response = test_client.post(
                "/update_employee_info/",
                json={
                    "email": 5,
                    "remember_me": False
                }
            )
            assert response.status_code == 400

            response = test_client.post(
                "/update_employee_info/",
                json={
                    "account_image": 5,
                    "remember_me": False
                }
            )
            assert response.status_code == 400

class TestToggleReview():
    def test_toggle_review_success(self, test_client, test_db):
        review_obj = db.session.query(Review).first()
        initial_shown = review_obj.shown

        with auth_handler(test_client):
            response = test_client.post(
                "/toggle_review/",
                json={
                    "id": review_obj.id,
                }
            )
            assert response.status_code == 200

        review_obj = db.session.query(Review).filter_by(id=review_obj.id).first()
        second_shown = review_obj.shown

        with auth_handler(test_client):
            response = test_client.post(
                "/toggle_review/",
                json={
                    "id": review_obj.id,
                }
            )
            assert response.status_code == 200

        review_obj = db.session.query(Review).filter_by(id=review_obj.id).first()
        last_shown = review_obj.shown

        assert initial_shown != second_shown
        assert initial_shown == last_shown

    def test_toggle_review_fail(self, test_client, test_db):
        review_obj = db.session.query(Review).first()

        # Non-Auth Tests
        response = test_client.post(
            "/toggle_review/",
            json={
                "id": review_obj.id,
            }
        )
        assert response.status_code == 302

        response = test_client.post(
            "/toggle_review/",
            json={
                "id": review_obj.id,
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'<div id="app">' in response.data

        with auth_handler(test_client):
            # Invalid type test
            response = test_client.post(
                "/toggle_review/",
                json={
                    "id": "test"
                }
            )
            assert response.status_code == 400

class TestGetLists():
    def test_get_supplier_list_success(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/get_supplier_list/"
            )
            assert response.status_code == 200
            assert len(json.loads(response.data.decode("utf-8"))["result"]) > 0

    def test_get_supplier_list_fail(self, test_client, test_db):
        response = test_client.post(
            "/get_supplier_list/"
        )
        assert response.status_code == 302

        response = test_client.post(
            "/get_supplier_list/",
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'<div id="app">' in response.data

    def test_get_part_list_success(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/get_part_list/"
            )
            assert response.status_code == 200
            assert len(json.loads(response.data.decode("utf-8"))["result"]) > 0

    def test_get_part_list_fail(self, test_client, test_db):
        response = test_client.post(
            "/get_part_list/"
        )
        assert response.status_code == 302

        response = test_client.post(
            "/get_part_list/",
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'<div id="app">' in response.data

    def test_get_category_list_success(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/get_category_list/"
            )
            assert response.status_code == 200
            assert len(json.loads(response.data.decode("utf-8"))["result"]) > 0

    def test_get_category_list_fail(self, test_client, test_db):
        response = test_client.post(
            "/get_category_list/"
        )
        assert response.status_code == 302

        response = test_client.post(
            "/get_category_list/",
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'<div id="app">' in response.data

# ! Need update_employee_info() remember_me test
