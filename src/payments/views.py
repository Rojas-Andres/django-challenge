from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.serializers import PaymentSerializer, PaymentUpdateSerializer
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


class PaymentStatusView(APIView):
    """
    API endpoint for activating a loan.

    Methods:
        put: Activate a loan.
    """

    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        Activate a loan.

        Parameters:
            request: HTTP request.
            format: Format suffix.

        Returns:
            Response: HTTP response.
        """
        try:
            serializer = PaymentUpdateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=422)
            PaymentService.update_payment_status(request.data["external_id"], request.data["status"])
            return Response(
                {
                    "message": "Pago actualizado correctamente",
                },
                status=200,
            )
        except ValidationError as value_error:
            return Response(
                value_error.detail,
                status=422,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=500,
            )
