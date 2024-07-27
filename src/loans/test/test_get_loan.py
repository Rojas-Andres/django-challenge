from datetime import datetime

import django
from django.urls import reverse
from django.utils import timezone
from customers.models import Customer
from loans.models import Loan
from test.test_setup import TestSetup


class TestGetLoans(TestSetup):
    @classmethod
    def setUpClass(cls) -> None:
        super(TestGetLoans, cls).setUpClass()
        django.setup()

    def setUp(self):
        super().setUp()
        self.url_loan = reverse("loans:loan")

        customer = Customer.objects.create(external_id="12", status=1, score=10000, preapproved_at=timezone.now())

        Loan.objects.create(
            customer=customer,
            external_id="12-1",
            amount=1000,
            status=1,
            created_at=datetime.now(),
        )
        Loan.objects.create(
            customer=customer,
            amount=12,
            external_id="12-2",
            status=2,
            created_at=datetime.now(),
        )

    def test_get_loan(self):
        """
        Test case for retrieving loans using the GET method.

        This test sends a GET request to the specified URL and checks if the response
        status code is 200 (OK) and if the number of loan results in the response JSON
        is equal to 2.

        """
        response = self.client_auth.get(self.url_loan)
        assert response.status_code == 200
        assert len(response.json()["results"]) == 2

    def test_get_filter_status_loan(self):
        """
        Test case to verify the filtering of loans based on status.

        This test sends two requests to the loan endpoint with different status values.
        It asserts that the response status code is 200 and the number of results in the response is 1 for each status value.
        """
        query_params = {"status": 1}
        response = self.client_auth.get(self.url_loan, query_params)
        assert response.status_code == 200
        assert len(response.json()["results"]) == 1

        query_params_2 = {"status": 2}
        response_status_2 = self.client_auth.get(self.url_loan, query_params_2)
        assert response_status_2.status_code == 200
        assert len(response_status_2.json()["results"]) == 1

    def test_get_filter_external_id(self):
        """
        Test case to verify the behavior of filtering loans by external ID.

        This test sends a GET request to the loan endpoint with a query parameter
        'external_id' set to '12-2'. It then asserts that the response status code
        is 200 (OK) and that the number of results in the response JSON is 1.

        """
        query_params = {"external_id": "12-2"}
        response = self.client_auth.get(self.url_loan, query_params)
        assert response.status_code == 200
        assert len(response.json()["results"]) == 1

    def test_get_filter_customer_external_id(self):
        """
        Test case to verify the filtering of loans by customer external ID.

        It creates a customer with external ID "13" and creates 10 loans associated with that customer.
        Then, it sends a GET request to the loan endpoint with query parameter "customer_external_id" set to "13".
        The test asserts that the response status code is 200 and the number of loan results in the response is 10.
        """
        customer_2 = Customer.objects.create(external_id="13", status=1, score=10000, preapproved_at=timezone.now())
        for i in range(10):
            Loan.objects.create(
                customer=customer_2,
                amount=1000,
                external_id=f"13-{i}",
                status=1,
                created_at=datetime.now(),
            )
        query_params = {"customer_external_id": "13"}
        response = self.client_auth.get(self.url_loan, query_params)
        assert response.status_code == 200
        assert len(response.json()["results"]) == 10
