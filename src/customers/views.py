from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.factory import ProcessingFactory
from customers.filters import CustomerFilters
from customers.models import Customer
from customers.serializers import CustomerSerializer, CustomerSerializerBalance
from utils.pagination import StandardResultsSetPagination


class CustomerViewTemplate(GenericAPIView):
    serializer_class = CustomerSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    pagination_class = StandardResultsSetPagination
    page_size_query_param = "page_size"
    ordering_fields = ["created_at", "updated_at"]
    permission_classes = [IsAuthenticated]
    filterset_class = CustomerFilters

    def get_queryset(self):
        """
        Override get_queryset to allow filtering by attorney_client

        Returns:
            Queryset: Queryset of ClientDiary objects
        """
        get_queryset = Customer.objects.filter(deleted_at=None)
        return get_queryset

    def get(self, request):
        """Handle GET request."""
        filterset = self.filterset_class(data=request.query_params, queryset=self.get_queryset())
        try:
            filtered_queryset = filterset.qs
        except ValueError as value_error:
            return Response(
                {"error": str(value_error)},
                status=422,
            )
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(filtered_queryset, request)
        serializer = self.serializer_class(page, many=True)

        return paginator.get_paginated_response(serializer.data)


class CustomerView(CustomerViewTemplate):
    """View for retrieving the created appointment."""

    def post(self, request):
        """Handle POST request."""
        try:
            processing_type = request.query_params.get("processing_type")
            response = ProcessingFactory.processing(strategy_name=processing_type, request=request)
            return Response(response)
        except ValidationError as validation_error:
            return Response(
                validation_error.detail,
                status=422,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=500,
            )


class CustomerBalanceView(CustomerViewTemplate):
    """
    API endpoint for retrieving the balance of all customers.

    Methods:
        get: Retrieve the balance of all customers.
    """

    serializer_class = CustomerSerializerBalance
