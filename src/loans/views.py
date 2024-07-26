from rest_framework.views import APIView
from rest_framework.response import Response
from loans.serializers import LoanSerializer, LoanUpdateSerializer
from django.db.models import Sum
from customers.models import Customer
from utils.messages import MESSAGE_LOAN_CREATE
from loans.services import LoanService
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated


class LoanView(APIView):
    """View for retrieving the created appointment."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Handle POST request."""
        try:
            serializer = LoanSerializer(data=request.data)
            if serializer.is_valid():
                customer: Customer = serializer.validated_data["customer"]
                total_debt = customer.loans.filter(status__in=[1, 2]).aggregate(Sum("amount"))["amount__sum"] or 0
                if total_debt + serializer.validated_data["amount"] > customer.score:
                    return Response(
                        {
                            "error": MESSAGE_LOAN_CREATE.format(
                                custom_score=customer.score, debt=total_debt, max_debt=customer.score - total_debt
                            )
                        },
                        status=422,
                    )
                serializer.save()
                response = {**serializer.data, "customer_external_id": customer.external_id}
                return Response(response, status=201)
            return Response(serializer.errors, status=422)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=500,
            )


class LoanStatusLoan(APIView):
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
            serializer = LoanUpdateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=422)
            result = LoanService.activate_loan(request.data)
            return Response(result, status=200)
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
