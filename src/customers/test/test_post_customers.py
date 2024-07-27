from datetime import datetime

import django
from django.core.management import call_command
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase
from test.test_setup import TestSetup
from customers.models import Customer
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class TestCreateCustomers(TestSetup):
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
        response = self.client_auth.post(f"{self.url}?processing_type=xml", body)
        assert response.status_code == 422

    def test_auth_create_customer_validate(self):
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
        assert response.status_code == 401

    def test_create_customer_json_success(self):
        """
        Test case to verify the successful creation of a customer using JSON format.

        This test sends a POST request to the specified URL with a JSON payload containing customer details.
        It checks if the response status code is 200, indicating a successful creation.

        Returns:
            None
        """
        body = {
            "customers": [
                {
                    "external_id": "12",
                    "status": 1,
                    "score": 100,
                    "preapproved_at": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            ]
        }
        response = self.client_auth.post(f"{self.url}?processing_type=json", body, format="json")
        assert response.status_code == 200

    def test_create_customer_json_failed(self):
        """
        Test case for creating a customer with JSON data that fails.

        This test case sends a POST request to create a customer with JSON data that fails to meet the required format.
        It verifies that the response status code is 200, indicating a successful request.

        """
        body = {
            "customers": [
                {
                    "external_id": "12",
                    "preapproved_at": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            ]
        }
        response = self.client_auth.post(f"{self.url}?processing_type=json", body, format="json")
        assert response.status_code == 422

    def test_create_customer_txt_success(self):
        """
        Test case for creating a customer with JSON data that fails.

        This test case sends a POST request to create a customer with JSON data that fails to meet the required format.
        It verifies that the response status code is 200, indicating a successful request.

        """
        file_path = os.path.join(os.path.dirname(__file__), "mock_data", "data_customers.txt")
        with open(file_path, "rb") as f:
            file = SimpleUploadedFile(f.name, f.read(), content_type="text/plain")

            response = self.client_auth.post(f"{self.url}?processing_type=txt", {"file": file}, format="multipart")
            assert response.status_code == 200

    def test_create_customer_txt_failed(self):
        """
        Test case for creating a customer with JSON data that fails.

        This test case sends a POST request to create a customer with JSON data that fails to meet the required format.
        It verifies that the response status code is 200, indicating a successful request.

        """
        file_path = os.path.join(os.path.dirname(__file__), "mock_data", "data_customers_failed.txt")
        with open(file_path, "rb") as f:
            file = SimpleUploadedFile(f.name, f.read(), content_type="text/plain")

            response = self.client_auth.post(f"{self.url}?processing_type=txt", {"file": file}, format="multipart")
            assert response.status_code == 422
            assert response.json() == [{"preapproved_at": ["This field is required."]}]
