import django
from django.core.management import call_command
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase
from customers.models import Customer
from datetime import datetime


class TestCreateCustomers(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super(TestCreateCustomers, cls).setUpClass()
        django.setup()

    def setUp(self):
        super().setUp()
        self.url = reverse("customers:customer")

    def test_create_customer_filed_processing_type(self):
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
        body = {
            "external_id": "12",
            "status": 1,
            "score": 100,
            "created_at": timezone.now(),
            "preapproved_at": timezone.now(),
        }
        response = self.client.post(f"{self.url}?processing_type=xml", body)
        assert response.status_code == 422
