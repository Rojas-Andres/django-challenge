from django.db import models

from core.models import BaseModel
from customers.models import Customer
from loans.models import Loan

STATUS_PAYMENTS = (
    (1, "completed"),
    (2, "rejected"),
)


class Payment(BaseModel):
    """Payment model."""

    external_id = models.CharField(max_length=60, unique=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=10)
    status = models.SmallIntegerField(choices=STATUS_PAYMENTS, default=1)
    paid_at = models.DateTimeField(null=True, blank=True)
    customer = models.ForeignKey(Customer, related_name="payments", on_delete=models.CASCADE)


class PaymentDetail(BaseModel):
    """
    Payment detail model.
    """

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment = models.ForeignKey(Payment, related_name="details", on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, related_name="payment_details", on_delete=models.CASCADE)
