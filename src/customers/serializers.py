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
    Serializer class for representing customer balance information.

    This serializer calculates the available amount and total debt for a customer
    based on their score and outstanding loans.

    Attributes:
        model (Customer): The Customer model class.
        fields (list): The list of fields to include in the serialized representation.

    Methods:
        to_representation(instance): Converts the instance to a serialized representation.

    """

    class Meta:
        model = Customer
        fields = ["external_id", "status", "score", "preapproved_at"]

    def to_representation(self, instance):
        """
        Converts the given instance into a representation that can be serialized.

        Args:
            instance: The instance of the customer model.

        Returns:
            A dictionary containing the serialized representation of the instance,
            including the external ID, score, available amount, and total debt.
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
