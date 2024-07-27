from django.db import models

from core.models import BaseModel
from customers.models import Customer

STATUS_LOAN = (
    (1, "pending"),
    (2, "active"),
    (3, "rejected"),
    (4, "paid"),
)


class Loan(BaseModel):
    """
    Represents a loan in the system.

    Attributes:
        external_id (str): The unique identifier for the loan.
        amount (Decimal): The amount of the loan.
        contract_version (str, optional): The version of the loan contract.
        status (int, optional): The status of the loan.
        outstanding (Decimal, optional): The outstanding balance of the loan.
        taken_at (datetime, optional): The date and time when the loan was taken.
        customer (Customer): The customer associated with the loan.
    """

    external_id = models.CharField(max_length=60, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    contract_version = models.CharField(max_length=30, blank=True, null=True)
    status = models.SmallIntegerField(choices=STATUS_LOAN, default=1)
    outstanding = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taken_at = models.DateTimeField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
