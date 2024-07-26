from datetime import datetime

import django
from django.urls import reverse
from django.utils import timezone
from customers.models import Customer
from test.test_setup import TestSetup
from faker import Faker

fake = Faker()


class TestGetCustomers(TestSetup):
    @classmethod
    def setUpClass(cls) -> None:
        super(TestGetCustomers, cls).setUpClass()
        django.setup()

    def setUp(self):
        super().setUp()
        # self.url_auth = reverse("authentication:logout")
        self.url_create_user = reverse("user:user_create")

    def test_login_user_success(self):
        """
        Test case to verify successful user login.

        This test case performs the following steps:
        1. Creates a new user with a fake email, password, first name, and last name.
        2. Sends a POST request to the login endpoint with the created user's email and password.
        3. Asserts that the response status code is 200 (OK).
        4. Asserts that the response data contains a "token" key.

        If all assertions pass, it indicates that the user login was successful.
        """
        email_fake = fake.email()
        body = {"email": email_fake, "password": "123456", "first_name": "Andres", "last_name": "Rojas"}
        response = self.client.post(self.url_create_user, body)
        assert response.status_code == 201

        body = {"email": email_fake, "password": "123456"}
        response = self.client.post(reverse("authentication:login"), body)
        assert response.status_code == 200
        assert "token" in response.data
