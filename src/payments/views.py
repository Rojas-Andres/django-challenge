from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payments.serializers import PaymentSerializer
from payments.services import PaymentService
from utils.views_template import ViewTemplateFilters


class PaymentView(ViewTemplateFilters):
    """View for retrieving the created appointment."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Handle POST request."""
        try:
            serializer = PaymentSerializer(data=request.data)
            if serializer.is_valid():
                payments_detail = serializer.validated_data
                PaymentService.validate_loan_payment_amount(payments_detail=payments_detail["payment_detail"])
                PaymentService.create_payment(
                    payment=payments_detail["payment"], payment_details=payments_detail["payment_detail"]
                )
                return Response(
                    {
                        "message": "Pago realizado con éxito.",
                    },
                    status=201,
                )
            return Response(serializer.errors, status=422)
        except ValidationError as validation_error:
            return Response(
                {"errors": validation_error.detail},
                status=422,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=500,
            )
