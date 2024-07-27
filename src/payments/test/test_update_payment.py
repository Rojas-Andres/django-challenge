from test.test_setup import TestSetup

import django
from django.urls import reverse
from django.utils import timezone

from customers.models import Customer
from loans.models import Loan


class TestUpdatePayment(TestSetup):
    @classmethod
    def setUpClass(cls) -> None:
        super(TestUpdatePayment, cls).setUpClass()
        django.setup()

    def setUp(self):
        super().setUp()
        self.url = reverse("payments:payment")
        self.url_status = reverse("payments:payment_status")
        self.customer = Customer.objects.create(external_id="12", status=1, score=10000, preapproved_at=timezone.now())
        self.loan = Loan.objects.create(
            external_id="loan_external-1", amount=1000, outstanding=1000, status=2, customer=self.customer
        )
        self.loan_pending = Loan.objects.create(
            external_id="loan_external-2", amount=1000, outstanding=1000, status=1, customer=self.customer
        )

    def test_update_status_payment_rejected(self):
        """
        Test case to verify the successful update of a payment status to rejected.
        """
        body_payment = {
            "payment_detail": [
                {
                    "amount": 55,
                    "loan_external_id": "loan_external-1",
                },
            ],
            "payment": {
                "external_id": "123",
                "customer_external_id": "12",
            },
        }
        response = self.client_auth.post(self.url, body_payment, format="json")
        assert response.status_code == 201
        assert response.json() == {"message": "Pago realizado con éxito."}
        response_update = self.client_auth.put(self.url_status, {"external_id": "123", "status": 1}, format="json")
        assert response_update.status_code == 422
        assert response_update.json() == {"error": "El pago ya esta en ese estado"}

        response_update_rejected = self.client_auth.put(
            self.url_status, {"external_id": "123", "status": 2}, format="json"
        )
        assert response_update_rejected.status_code == 200
        assert response_update_rejected.json() == {"message": "Pago actualizado correctamente"}

        response_update_rejected_failed = self.client_auth.put(
            self.url_status, {"external_id": "123", "status": 1}, format="json"
        )
        assert response_update_rejected_failed.status_code == 422
        assert response_update_rejected_failed.json() == {
            "error": "El pago no se puede actualizar a active porque esta en active"
        }
