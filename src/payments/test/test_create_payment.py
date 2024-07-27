import django
from django.urls import reverse
from django.utils import timezone
from customers.models import Customer
from loans.models import Loan
from test.test_setup import TestSetup


class TestCreatePayment(TestSetup):
    @classmethod
    def setUpClass(cls) -> None:
        super(TestCreatePayment, cls).setUpClass()
        django.setup()

    def setUp(self):
        super().setUp()
        self.url = reverse("payments:payment")
        self.customer = Customer.objects.create(external_id="12", status=1, score=10000, preapproved_at=timezone.now())
        self.loan = Loan.objects.create(
            external_id="loan_external-1", amount=1000, outstanding=1000, status=2, customer=self.customer
        )
        self.loan_pending = Loan.objects.create(
            external_id="loan_external-2", amount=1000, outstanding=1000, status=1, customer=self.customer
        )

    def test_customer_not_found_create_payment(self):
        """
        Test case to verify that a payment cannot be created if the customer does not exist.
        """
        body_payment = {
            "payment_detail": [
                {
                    "amount": 1000,
                    "loan_external_id": "123",
                }
            ],
            "payment": {
                "external_id": "123",
                "customer_external_id": "1",
            },
        }
        response = self.client_auth.post(self.url, body_payment, format="json")
        assert response.status_code == 422
        assert response.json()["payment"] == {"customer_external_id": ["El customer_external_id 1 no existe."]}

    def test_loan_not_found_create_payment(self):
        """
        Test case to verify that a payment cannot be created if the loan_external_id does not exist.
        """
        body_payment = {
            "payment_detail": [
                {
                    "amount": 1000,
                    "loan_external_id": "123",
                }
            ],
            "payment": {
                "external_id": "123",
                "customer_external_id": "12",
            },
        }
        response = self.client_auth.post(self.url, body_payment, format="json")
        assert response.status_code == 422
        assert response.json() == {"payment_detail": [{"loan_external_id": ["El load_external_id 123 no existe."]}]}

    def test_invalid_amount_to_create_payment(self):
        """
        Test case to verify that an invalid payment amount raises the expected error.

        The test sends a request to create a payment with an amount that is greater than the pending loan balance.
        It expects the response status code to be 422 (Unprocessable Entity) and the response JSON to contain an error message
        indicating that the payment amount cannot be greater than the pending loan balance.

        This test helps ensure that the payment creation endpoint correctly handles invalid payment amounts.

        """
        body_payment = {
            "payment_detail": [
                {
                    "amount": 999999999,
                    "loan_external_id": "loan_external-1",
                }
            ],
            "payment": {
                "external_id": "123",
                "customer_external_id": "12",
            },
        }
        response = self.client_auth.post(self.url, body_payment, format="json")
        assert response.status_code == 422
        assert response.json()["errors"] == [
            "El monto del pago no puede ser mayor que el saldo pendiente del préstamo.saldo_pendiente = 1000.00 y monto_del_pago = 999999999"
        ]

    def test_duplicate_loan_payment(self):
        """
        Test case to verify that duplicate loan payments are handled correctly.

        This test sends a POST request to the specified URL with a payment body that contains
        two payment details with the same loan_external_id. The test expects the response status
        code to be 422 (Unprocessable Entity) and the response JSON to contain an error message
        indicating the presence of a duplicate loan_external_id.

        """
        body_payment = {
            "payment_detail": [
                {
                    "amount": 55,
                    "loan_external_id": "loan_external-1",
                },
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
        assert response.status_code == 422
        assert response.json()["payment_detail"] == ["Duplicate load_external_id found: loan_external-1"]

    def test_loan_pending_not_create_payment(self):
        """
        Test case to verify that a payment cannot be created when the loan is not active.

        This test sends a POST request to the specified URL with a payment payload that includes a loan_external_id
        for a loan that is not in an active state. The test expects the response status code to be 422 (Unprocessable Entity)
        and the response body to contain an error message indicating that the loan is not active.

        """
        body_payment = {
            "payment_detail": [
                {
                    "amount": 55,
                    "loan_external_id": "loan_external-2",
                },
            ],
            "payment": {
                "external_id": "123",
                "customer_external_id": "12",
            },
        }
        response = self.client_auth.post(self.url, body_payment, format="json")
        assert response.status_code == 422
        assert response.json()["payment_detail"] == [
            {"loan_external_id": ["El estado del prestamo no esta activo por lo tanto no se puede realizar el pago."]}
        ]

    def test_negative_payment(self):
        """
        Test case to verify that a negative payment amount returns a 422 status code
        and the appropriate error message in the response.
        """
        body_payment = {
            "payment_detail": [
                {
                    "amount": -55,
                    "loan_external_id": "loan_external-1",
                },
            ],
            "payment": {
                "external_id": "123",
                "customer_external_id": "12",
            },
        }
        response = self.client_auth.post(self.url, body_payment, format="json")
        assert response.status_code == 422
        assert response.json()["payment_detail"] == [{"amount": ["El monto no puede ser negativo"]}]

    def test_payment_create_success(self):
        """
        Test case to verify successful creation of a payment.

        This test sends a POST request to the specified URL with a payment payload.
        It asserts that the response status code is 201 (Created) and the response JSON
        matches the expected message indicating successful payment creation.
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
        assert response.json() == {'message': 'Pago realizado con éxito.'}

    def test_error_duplicate_payment(self):
        """
        Test case to verify the behavior when a duplicate payment is made.

        This test sends a payment request with the same external_id as an existing payment.
        It expects the server to return a 422 status code and a specific error message.

        Steps:
        1. Create a payment request with a specific external_id and customer_external_id.
        2. Send the payment request to the server.
        3. Verify that the response status code is 201 (indicating success).
        4. Verify that the response JSON message is 'Pago realizado con éxito.' (Payment made successfully).
        5. Create another payment request with the same external_id and customer_external_id.
        6. Send the second payment request to the server.
        7. Verify that the response status code is 422 (indicating a validation error).
        8. Verify that the response JSON contains the expected error message for the payment field.

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
        assert response.json() == {'message': 'Pago realizado con éxito.'}
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
        assert response.status_code == 422
        assert response.json()["payment"] == {'external_id': ['El external_id 123 ya existe con el pago.']}