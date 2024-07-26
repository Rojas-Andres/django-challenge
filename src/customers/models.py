from core.models import BaseModel
from django.db import models

STATUS_CUSTOMER = [
    (1, "Activo"),
    (2, "Inactivo"),
]


class Customer(BaseModel):
    """
    Represents a customer in the system.

    Attributes:
        extenal_id (str): The external ID of the customer.
        status (int): The status of the customer.
        score (Decimal): The score of the customer.
        preapproved_at (datetime): The datetime when the customer was preapproved.
    """

    external_id = models.CharField(max_length=60, unique=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CUSTOMER, default=1)
    score = models.DecimalField(max_digits=12, decimal_places=2)
    preapproved_at = models.DateTimeField(null=False, blank=False)
