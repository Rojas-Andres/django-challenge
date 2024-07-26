from django.shortcuts import render
from rest_framework.views import APIView
from customers.factory import ProcessingFactory
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from customers.serializers import CustomerSerializer
from utils.pagination import StandardResultsSetPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from customers.models import Customer
from customers.filters import CustomerFilters
from rest_framework.generics import GenericAPIView


class CustomerView(GenericAPIView):
    """View for retrieving the created appointment."""

    serializer_class = CustomerSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    pagination_class = StandardResultsSetPagination
    page_size_query_param = "page_size"
    ordering_fields = ["created_at", "updated_at"]

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
