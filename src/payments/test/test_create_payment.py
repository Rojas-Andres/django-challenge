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
        Test case for creating a payment.

        This test case verifies that a payment can be successfully created by sending a POST request to the specified URL
        with the required parameters. It checks that the response status code is 201, indicating a successful creation.

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
        Test case for creating a payment.

        This test case verifies that a payment can be successfully created by sending a POST request to the specified URL
        with the required parameters. It checks that the response status code is 201, indicating a successful creation.

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
        Test case for creating a payment.

        This test case verifies that a payment can be successfully created by sending a POST request to the specified URL
        with the required parameters. It checks that the response status code is 201, indicating a successful creation.

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
        Test case for creating a payment.

        This test case verifies that a payment can be successfully created by sending a POST request to the specified URL
        with the required parameters. It checks that the response status code is 201, indicating a successful creation.

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
        Test case for creating a payment.

        This test case verifies that a payment can be successfully created by sending a POST request to the specified URL
        with the required parameters. It checks that the response status code is 201, indicating a successful creation.

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
        Test case for creating a payment.

        This test case verifies that a payment can be successfully created by sending a POST request to the specified URL
        with the required parameters. It checks that the response status code is 201, indicating a successful creation.

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