from django.shortcuts import render
from rest_framework.views import APIView
from customers.factory import ProcessingFactory
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


class CustomerView(APIView):
    """View for retrieving the created appointment."""

    def post(self, request):
        """Handle POST request."""
        try:
            processing_type = request.query_params.get("processing_type")
            response = ProcessingFactory.processing(strategy_name=processing_type, request=request)
            return Response(response)
        except ValidationError as validation_error:
            return Response(
                str(validation_error),
                status=422,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=500,
            )
