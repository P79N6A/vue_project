from contextlib import contextmanager

import pytest

from app import create_app
import app.settings as settings
from ..models import Employee
from admin.app.models import db

@contextmanager
def auth_handler(test_client, email="tester", password="password", expected_status=200):
    employee = db.session.query(Employee).filter_by(email="tester").first()
    if employee is None:
        employee = Employee("tester", "$2y$12$RtQDOi1pJzC/ibKFZyklLunNuz4HktJtmj79bIaVeBm1Cxp2YP2sy")
        db.session.add(employee)
        db.session.commit()

    response = test_client.post(
        "/login/",
        json={
            "email": email,
            "password": password
        }
    )
    assert response.status_code == expected_status

    with test_client.session_transaction() as sess:
        if expected_status == 200:
            assert sess["email"] == "tester"
        else:
            assert "email" not in sess

    yield

    response = test_client.post(
        "/logout/"
    )
    assert response.status_code == 200

    with test_client.session_transaction() as sess:
        assert "email" not in sess
