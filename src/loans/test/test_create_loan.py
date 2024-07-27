from datetime import datetime

import django
from django.urls import reverse
from django.utils import timezone
from customers.models import Customer
from test.test_setup import TestSetup


class TestCreateLoans(TestSetup):
    @classmethod
    def setUpClass(cls) -> None:
        super(TestCreateLoans, cls).setUpClass()
        django.setup()

    def setUp(self):
        super().setUp()
        self.url_loan = reverse("loans:loan")

        self.customer = Customer.objects.create(external_id="12", status=1, score=10000, preapproved_at=timezone.now())

    def test_create_loan(self):
        """
        Test case for creating a loan.

        This test case verifies that a loan can be successfully created by sending a POST request to the specified URL
        with the required parameters. It checks that the response status code is 201, indicating a successful creation.

        """
        body_loan = {
            "customer": self.customer.id,
            "amount": 1000,
            "external_id": "123",
        }
        response = self.client_auth.post(self.url_loan, body_loan, format="json")
        assert response.status_code == 201

    def test_create_loan_invalid(self):
        """
        Test case for creating a loan.

        This test case verifies that a loan can be successfully created by sending a POST request to the specified URL
        with the required parameters. It checks that the response status code is 201, indicating a successful creation.

        """
        body_loan = {
            "customer": self.customer.id,
            "amount": self.customer.score + 1,
            "external_id": "123",
        }
        response = self.client_auth.post(self.url_loan, body_loan, format="json")
        assert response.status_code == 422
        assert (
            response.json()["error"]
            == " The customer's score is not enough to request the loan. customer_score = 10000.00 and total_debt = 0, you can request a maximum of 10000.00 "
        )

    def test_create_loan_invalid_serializer(self):
        """
        Test case for creating a loan.

        This test case verifies that a loan can be successfully created by sending a POST request to the specified URL
        with the required parameters. It checks that the response status code is 201, indicating a successful creation.

        """
        body_loan = {
            "customer": self.customer.id,
            "external_id": "123",
        }
        response = self.client_auth.post(self.url_loan, body_loan, format="json")
        assert response.status_code == 422
        assert response.json() == {"amount": ["This field is required."]}
