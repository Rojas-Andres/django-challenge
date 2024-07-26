from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customers.factory import ProcessingFactory
from customers.filters import CustomerFilters
from customers.models import Customer
from customers.serializers import CustomerSerializer, CustomerSerializerBalance
from utils.pagination import StandardResultsSetPagination


class CustomerViewTemplate(GenericAPIView):
    """
    A view template for handling customer-related requests.

    This view template provides functionality for handling GET requests and returning
    paginated responses based on the provided query parameters. It also allows filtering
    by attorney_client.

    Attributes:
        serializer_class (Serializer): The serializer class for serializing/deserializing
            customer data.
        filter_backends (tuple): The filter backends to be used for filtering the queryset.
        pagination_class (Pagination): The pagination class for paginating the queryset.
        page_size_query_param (str): The query parameter for specifying the page size.
        ordering_fields (list): The fields that can be used for ordering the queryset.
        permission_classes (list): The permission classes required for accessing the view.
        filterset_class (FilterSet): The filterset class for filtering the queryset.

    Methods:
        get_queryset(): Override of the get_queryset method to allow filtering by attorney_client.
        get(request): Handle GET requests and return paginated response based on query parameters.
    """

    serializer_class = CustomerSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    pagination_class = StandardResultsSetPagination
    page_size_query_param = "page_size"
    ordering_fields = ["created_at", "updated_at"]
    permission_classes = [IsAuthenticated]
    filterset_class = CustomerFilters

    def get_queryset(self):
        """
        Override of the get_queryset method to allow filtering by attorney_client.

        Returns:
            QuerySet: The queryset of Customer objects.
        """
        get_queryset = Customer.objects.filter(deleted_at=None)
        return get_queryset

    def get(self, request):
        """
        Handle GET requests and return paginated response based on query parameters.

        This method is responsible for handling GET requests and returning a paginated
        response based on the provided query parameters. It applies filtering using the
        filterset_class and returns the paginated response containing serialized data.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The paginated response containing serialized data.

        Raises:
            ValueError: If there is an error in the provided query parameters.
        """
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
        """
        Handle HTTP POST requests.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response object.

        Raises:
            ValidationError: If there is a validation error.
            Exception: If there is an unexpected error.

        """
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
    A view for retrieving the balance of a customer.

    This view extends the `CustomerViewTemplate` class and uses the `CustomerSerializerBalance`
    serializer class for serializing the customer's balance.

    Attributes:
        serializer_class (class): The serializer class used for serializing the customer's balance.
    """

    serializer_class = CustomerSerializerBalance
