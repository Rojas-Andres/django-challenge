from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from customers.models import Customer
from loans.models import Loan
from payments.models import Payment, PaymentDetail
from utils.messages import (
    MESSAGE_AMOUNT_GREATHER,
    MESSAGE_PAYMENT_NOT_FOUND,
    MESSAGE_PAYMENT_STATUS,
    MESSAGE_PAYMENT_UPDATE_ACTIVE_REJECTED,
)


class PaymentService:
    @staticmethod
    def validate_loan_payment_amount(payments_detail: dict):
        """
        Validates the payment amount for each loan in the payments_detail.

        Args:
            payments_detail (dict): A dictionary containing payment details.

        Raises:
            ValidationError: If the payment amount is greater than the outstanding amount for a loan.

        Returns:
            None
        """
        loans = Loan.objects.filter(external_id__in=[payment["loan_external_id"] for payment in payments_detail])
        for payment in payments_detail:
            loan = loans.get(external_id=payment["loan_external_id"])
            if loan.outstanding < payment["amount"]:
                raise ValidationError(
                    MESSAGE_AMOUNT_GREATHER.format(
                        amount=payment["amount"],
                        outstanding=loan.outstanding,
                    )
                )

    @staticmethod
    @transaction.atomic
    def create_payment(payment: dict, payment_details: list = []):  # pylint: disable=W0102
        """
        Create a payment and its associated payment details.

        Args:
            payment (dict): A dictionary containing payment information.
            payment_details (list, optional): A list of dictionaries containing payment details. Defaults to [].

        Returns:
            bool: True if the payment and payment details are created successfully, False otherwise.
        """

        customer = Customer.objects.get(external_id=payment["customer_external_id"])
        payment_create = Payment.objects.create(
            customer=customer,
            paid_at=timezone.now(),
            status=1,
            total_amount=sum(payment["amount"] for payment in payment_details),
            external_id=payment["external_id"],
        )
        payment_create.save()
        for payment_detail in payment_details:
            loan = Loan.objects.get(external_id=payment_detail["loan_external_id"])
            payment_detail = PaymentDetail.objects.create(
                payment=payment_create,
                amount=payment_detail["amount"],
                loan=loan,
            )
            loan.outstanding -= payment_detail.amount
            payment_detail.save()
            loan.save()

    @staticmethod
    def update_payment_status(payment_external_id: str, status: int):
        payment = Payment.objects.filter(external_id=payment_external_id).first()
        if not payment:
            raise ValidationError({"error": MESSAGE_PAYMENT_NOT_FOUND})
        if payment.status == status:
            raise ValidationError({"error": MESSAGE_PAYMENT_STATUS})
        if payment.status == 2 and status == 1:
            raise ValidationError({"error": MESSAGE_PAYMENT_UPDATE_ACTIVE_REJECTED})
        payment.status = status
        payment.save()
