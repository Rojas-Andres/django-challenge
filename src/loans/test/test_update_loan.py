from datetime import datetime
from test.test_setup import TestSetup

import django
from django.urls import reverse
from django.utils import timezone

from customers.models import Customer


class TestGetLoans(TestSetup):
    @classmethod
    def setUpClass(cls) -> None:
        super(TestGetLoans, cls).setUpClass()
        django.setup()

    def setUp(self):
        super().setUp()
        self.url_loan = reverse("loans:loan")
        self.url_loan_update = reverse("loans:loan_status")
        self.customer = Customer.objects.create(external_id="12", status=1, score=10000, preapproved_at=timezone.now())

    def test_update_loan_success(self):
        """
        Test case to verify the successful update of a loan.

        This test case performs the following steps:
        1. Creates a new loan with the specified customer ID, amount, and external ID.
        2. Sends a PUT request to update the loan with the specified external ID and status.
        3. Asserts that the response status code is 200.
        4. Asserts that the response JSON matches the expected message.

        If all assertions pass, it indicates that the loan was successfully updated.

        Note: This test assumes the existence of a Django test client and the necessary setup
        for authentication and URLs.

        """
        external_loan_id = "123"
        body_loan = {
            "customer": self.customer.id,
            "amount": 1000,
            "external_id": external_loan_id,
        }
        response = self.client_auth.post(self.url_loan, body_loan, format="json")
        assert response.status_code == 201

        body_loan_update = {"external_id": external_loan_id, "status": 2}
        response_update = self.client_auth.put(self.url_loan_update, body_loan_update, format="json")
        assert response_update.status_code == 200
        assert response_update.json() == {"message": "Prestamo actualizado correctamente"}

    def test_update_loan_succes_doble_update_failed(self):
        """
        Test case to verify the behavior when attempting to update a loan twice.

        Steps:
        1. Create a new loan with a specific external loan ID.
        2. Update the loan status to 2 (some status value).
        3. Verify that the update is successful.
        4. Attempt to update the loan status to 3 (some other status value).
        5. Verify that the update fails with the appropriate error message.

        Expected behavior:
        - The first update should be successful.
        - The second update should fail with an error message indicating that the loan can only be modified if it is in the "pending" state.
        """
        external_loan_id = "123"
        body_loan = {
            "customer": self.customer.id,
            "amount": 1000,
            "external_id": external_loan_id,
        }
        response = self.client_auth.post(self.url_loan, body_loan, format="json")
        assert response.status_code == 201

        body_loan_update = {"external_id": external_loan_id, "status": 2}
        response_update = self.client_auth.put(self.url_loan_update, body_loan_update, format="json")
        assert response_update.status_code == 200
        assert response_update.json() == {"message": "Prestamo actualizado correctamente"}

        body_loan_update = {"external_id": external_loan_id, "status": 3}
        response_update_rejected = self.client_auth.put(self.url_loan_update, body_loan_update, format="json")
        assert response_update_rejected.status_code == 422
        assert response_update_rejected.json() == {
            "error": "Prestamo solo se puede modificar si esta en estado pending"
        }

    def test_update_loan_pending_to_pending(self):
        """
        Test case to verify that a loan in 'pending' status cannot be updated to 'pending' status.
        """
        external_loan_id = "123"
        body_loan = {
            "customer": self.customer.id,
            "amount": 1000,
            "external_id": external_loan_id,
        }
        response = self.client_auth.post(self.url_loan, body_loan, format="json")
        assert response.status_code == 201

        body_loan_update = {"external_id": external_loan_id, "status": 1}
        response_update = self.client_auth.put(self.url_loan_update, body_loan_update, format="json")
        assert response_update.status_code == 422
        assert response_update.json() == {
            "error": "El prestamo no se puede actualizar a pending porque esta en pending"
        }

    def test_update_loan_invalid(self):
        """
        Test case to verify the behavior when updating a loan with invalid data.

        This test sends a POST request to the specified URL with an invalid loan body.
        It then asserts that the response status code is 422 (Unprocessable Entity)
        and that the response JSON contains the expected error message for the 'external_id' field.

        """
        body_loan = {
            "customer": self.customer.id,
            "amount": 1000,
        }
        response = self.client_auth.post(self.url_loan, body_loan, format="json")
        assert response.status_code == 422
        assert response.json() == {"external_id": ["This field is required."]}
