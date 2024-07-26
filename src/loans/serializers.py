from rest_framework import serializers
from loans.models import Loan, STATUS_LOAN
from utils.messages import MESSAGE_AMOUNT_NOT_NEGATIVE, MESSAGE_STATUS_PERMISSION_LOAN


class LoanSerializer(serializers.ModelSerializer):
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
        model = Loan
        fields = ["external_id", "amount", "contract_version", "customer"]

    def validate_amount(self, value):
        """
        Check that the amount is not negative.
        """
        if value < 0:
            raise serializers.ValidationError(MESSAGE_AMOUNT_NOT_NEGATIVE)
        return value

    def create(self, validated_data):
        """
        Create a new loan instance and set the outstanding amount.

        Parameters:
            validated_data: Validated data for creating the loan.

        Returns:
            loan: The created Loan instance.
        """
        loan = Loan.objects.create(**validated_data)
        loan.outstanding = validated_data["amount"]
        loan.save()
        return loan


class LoanUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating loan information.

    Attributes:
        external_id (int): The external ID of the loan.
        status (int): The status of the loan.
    """

    external_id = serializers.CharField(required=True, max_length=60)
    status = serializers.IntegerField(required=True)

    def validate_status(self, value):
        """
        Check that the status is valid.
        """
        if value not in dict(STATUS_LOAN).keys():
            raise serializers.ValidationError(MESSAGE_STATUS_PERMISSION_LOAN.format(status=dict(STATUS_LOAN).keys()))
