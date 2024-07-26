from rest_framework import serializers

from customers.models import Customer
from loans.models import Loan


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for payments, including details and customer information.

    Fields:
        external_id: External ID of the payment.
        total_amount: Total amount of the payment.
        status: Status of the payment.
        customer_external_id: External ID of the customer (write-only).
        details: List of payment details.
    """

    class Meta:
        model = Customer
        fields = ["external_id", "status", "score", "preapproved_at"]


class CustomerSerializerBalance(serializers.ModelSerializer):
    """
    Serializer for payments, including details and customer information.

    Fields:
        external_id: External ID of the payment.
        total_amount: Total amount of the payment.
        status: Status of the payment.
        customer_external_id: External ID of the customer (write-only).
        details: List of payment details.
    """

    class Meta:
        model = Customer
        fields = ["external_id", "status", "score", "preapproved_at"]

    def to_representation(self, instance):
        """
        Customize the representation of the customer instance to include balance and debt information.

        Parameters:
            instance (Customer): The customer instance being serialized.

        Returns:
            dict: A dictionary containing the external_id, score, available amount, and total debt of the customer.
        """
        loans = Loan.objects.filter(customer=instance)
        total_debt = sum(loan.outstanding for loan in loans)
        available_amount = instance.score - total_debt

        return {
            "external_id": instance.external_id,
            "score": instance.score,
            "available_amount": available_amount,
            "total_debt": total_debt,
        }


class CustomerFileSerializer(serializers.Serializer):
    """
    Serializer for payments, including details and customer information.

    Fields:
        external_id: External ID of the payment.
        total_amount: Total amount of the payment.
        status: Status of the payment.
        customer_external_id: External ID of the customer (write-only).
        details: List of payment details.
    """

    file = serializers.FileField()
