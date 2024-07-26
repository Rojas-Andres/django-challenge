from datetime import datetime

import django
from django.urls import reverse
from django.utils import timezone
from customers.models import Customer
from test.test_setup import TestSetup


class TestGetCustomers(TestSetup):
    @classmethod
    def setUpClass(cls) -> None:
        super(TestGetCustomers, cls).setUpClass()
        django.setup()

    def setUp(self):
        super().setUp()
        self.url = reverse("customers:customer")

    def test_filter_status(self):
        """
        Test case to verify the filtering of customers based on status.

        This test creates two customer objects with different statuses and sends GET requests
        with different status parameters to the API endpoint. It then asserts the response
        status code and the number of results returned by the API.

        Assertions:
        - The first GET request with status=1 should return a single result with external_id="12".
        - The second GET request with status=2 should return a single result with external_id="1".
        - The third GET request with status="1,2" should return two results.

        """
        Customer.objects.create(
            external_id="12",
            status=1,
            score=100,
            created_at=timezone.now(),
            preapproved_at=timezone.now(),
        )
        Customer.objects.create(
            external_id="1",
            status=2,
            score=333,
            created_at=timezone.now(),
            preapproved_at=timezone.now(),
        )
        query_params = {
            "status": 1,
        }
        response_filter_1 = self.client_auth.get(self.url, query_params)
        assert response_filter_1.status_code == 200
        assert len(response_filter_1.json()["results"]) == 1
        assert response_filter_1.json()["results"][0]["external_id"] == "12"
        response_filter_2 = self.client_auth.get(
            self.url,
            {
                "status": 2,
            },
        )
        assert len(response_filter_2.json()["results"]) == 1
        assert response_filter_2.json()["results"][0]["external_id"] == "1"

        response_filter_3 = self.client_auth.get(
            self.url,
            {
                "status": "1,2",
            },
        )
        assert len(response_filter_3.json()["results"]) == 2

    def test_filter_external(self):
        """
        Test case to verify filtering customers by external_id.

        This test case creates 10 customers with different external_ids and then filters
        the customers using the external_id query parameter. It asserts that the response
        status code is 200, the number of results is 1, and the external_id of the first
        result matches the filtered external_id.

        """
        for i in range(10):
            Customer.objects.create(
                external_id=i,
                status=1,
                score=100,
                created_at=timezone.now(),
                preapproved_at=timezone.now(),
            )
        query_params = {
            "external_id": "3",
        }
        response_filter_1 = self.client_auth.get(self.url, query_params)
        assert response_filter_1.status_code == 200
        assert len(response_filter_1.json()["results"]) == 1
        assert response_filter_1.json()["results"][0]["external_id"] == "3"

    def test_filter_page(self):
        """
        Test case to verify filtering customers by external_id.

        This test case creates 10 customers with different external_ids and then filters
        the customers using the external_id query parameter. It asserts that the response
        status code is 200, the number of results is 1, and the external_id of the first
        result matches the filtered external_id.

        """
        for i in range(10):
            Customer.objects.create(
                external_id=i,
                status=1,
                score=100,
                created_at=timezone.now(),
                preapproved_at=timezone.now(),
            )
        query_params = {
            "page_size": 1,
        }
        response_filter_1 = self.client_auth.get(self.url, query_params)
        assert response_filter_1.status_code == 200
        assert len(response_filter_1.json()["results"]) == 1
        assert response_filter_1.json()["total_pages"] == 10

    def test_filter_preapproved(self):
        """
        Test case to verify the filtering of customers based on preapproval date.

        This test case creates three customer objects with different preapproval dates.
        It then sends GET requests to the specified URL with different preapproval dates as query parameters.
        The test asserts that the response status code is 200 and the number of results in the response matches the expected count.

        """
        Customer.objects.create(
            external_id="1221",
            status=1,
            score=100,
            created_at=timezone.now(),
            preapproved_at=datetime.strptime("2023-02-02 00:00:00", "%Y-%m-%d %H:%M:%S"),
        )
        Customer.objects.create(
            external_id="333",
            status=1,
            score=100,
            created_at=timezone.now(),
            preapproved_at=datetime.strptime("2023-02-05 00:00:00", "%Y-%m-%d %H:%M:%S"),
        )
        Customer.objects.create(
            external_id="421421",
            status=1,
            score=100,
            created_at=timezone.now(),
            preapproved_at=datetime.strptime("2023-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
        )
        query_params = {
            "preapproved_at": "2023-02-01",
        }
        response_filter_1 = self.client_auth.get(self.url, query_params)
        assert response_filter_1.status_code == 200
        assert len(response_filter_1.json()["results"]) == 2
        query_params = {
            "preapproved_at": "2023-02-04",
        }
        response_filter_2 = self.client_auth.get(self.url, query_params)
        assert response_filter_2.status_code == 200
        assert len(response_filter_2.json()["results"]) == 1

    def test_invalid_filter_at(self):
        """
        Test case to verify the filtering of customers based on preapproval date.

        This test case creates three customer objects with different preapproval dates.
        It then sends GET requests to the specified URL with different preapproval dates as query parameters.
        The test asserts that the response status code is 200 and the number of results in the response matches the expected count.

        """
        query_params = {
            "preapproved_at": "2023-02-01 4",
        }
        response_filter_1 = self.client_auth.get(self.url, query_params)
        assert response_filter_1.status_code == 422
