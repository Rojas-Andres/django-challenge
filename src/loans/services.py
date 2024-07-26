from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import Loan


class LoanService:
    @staticmethod
    def activate_loan(data: dict):
        loan = Loan.objects.filter(external_id=data["external_id"]).first()
        if not loan:
            raise ValidationError({"error": "Prestamo no encontrado"})
        if loan.status != 1:
            raise ValidationError({"error": "Prestamo solo se puede modificar si esta en estado pending"})
        if data["status"] == 1 and loan.status == 1:
            raise ValidationError({"error": "El prestamo no se puede actualizar a pending porque esta en pending"})
        if data["status"] == 2:
            loan.taken_at = timezone.now()
        loan.status = data["status"]
        loan.save()
        return {"message": "Prestamo actualizado correctamente"}
