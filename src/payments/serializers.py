from rest_framework import serializers

from customers.models import Customer
from loans.models import Loan
from payments.models import Payment
from utils.messages import (
    MESSAGE_AMOUNT_NOT_NEGATIVE,
    MESSAGE_CUSTOMER_EXTERNAL_ID_NOT_FOUND,
    MESSAGE_EXTERNAL_ID_DUPLICATE,
    MESSAGE_LOAD_EXTERNAL_ID_NOT_FOUND,
    MESSAGE_NOT_PERMISSION_PAYMENT,
    MESSAGE_PAYMENT_EXTERNAL_ID_EXISTS,
)


class PaymentDetailSerializer(serializers.Serializer):
    loan_external_id = serializers.CharField(max_length=60)
    amount = serializers.IntegerField()

    def validate_load_external_id(self, value):
        """
        Verifica que el loan ID exista en el modelo Loan.
        """
        loan = Loan.objects.filter(external_id=value).first()
        if not loan:
            raise serializers.ValidationError(MESSAGE_LOAD_EXTERNAL_ID_NOT_FOUND.format(value=value))
        if loan.status != 2:
            raise serializers.ValidationError(MESSAGE_NOT_PERMISSION_PAYMENT)
        return value

    def validate_amount(self, value):
        """
        Check that the amount is not negative.
        """
        if value < 0:
            raise serializers.ValidationError(MESSAGE_AMOUNT_NOT_NEGATIVE)
        return value


class PaymentOnly(serializers.Serializer):
    external_id = serializers.CharField(max_length=60)
    customer_external_id = serializers.CharField(max_length=60)

    def validate_external_id(self, value):
        """
        Verifica que el loan ID exista en el modelo Loan.
        """
        payment = Payment.objects.filter(external_id=value).first()
        if payment:
            raise serializers.ValidationError(MESSAGE_PAYMENT_EXTERNAL_ID_EXISTS.format(external_id=value))
        return value

    def validate_customer_external_id(self, value):
        """
        Verifica que el customer ID exista en el modelo Customer.
        """
        customer = Customer.objects.filter(external_id=value).first()
        if not customer:
            raise serializers.ValidationError(MESSAGE_CUSTOMER_EXTERNAL_ID_NOT_FOUND.format(value=value))
        return value


class PaymentSerializer(serializers.Serializer):
    """
    Serializer class for Payment objects.

    Attributes:
        payment (PaymentOnly): The payment object to be serialized.
        payment_detail (PaymentDetailSerializer): The payment detail objects to be serialized.
    """

    payment = PaymentOnly()
    payment_detail = PaymentDetailSerializer(many=True)

    def validate_payment_detail(self, value):
        """
        Validates the payment detail.

        Args:
            value (list): The payment detail to be validated.

        Returns:
            list: The validated payment detail.

        Raises:
            serializers.ValidationError: If there are duplicate external IDs in the payment detail.
        """
        seen_ids = set()
        for detail in value:
            load_external_id = detail.get("load_external_id")
            if load_external_id in seen_ids:
                raise serializers.ValidationError(
                    MESSAGE_EXTERNAL_ID_DUPLICATE.format(load_external_id=load_external_id)
                )
            seen_ids.add(load_external_id)
        return value
