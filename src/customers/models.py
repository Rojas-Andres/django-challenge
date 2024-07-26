from core.models import BaseModel
from django.db import models

STATUS_CUSTOMER = [
    (1, "Activo"),
    (2, "Inactivo"),
]


class Customer(BaseModel):
    """Customer model."""

    extenal_id = models.CharField(max_length=60, unique=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CUSTOMER)
    score = models.DecimalField(max_digits=12, decimal_places=2)
    preapproved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """Return string representation of customer."""
        return f"id={self.id} extenal_id={self.extenal_id} "
