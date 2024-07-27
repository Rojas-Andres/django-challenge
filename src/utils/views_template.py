from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.pagination import StandardResultsSetPagination


class ViewTemplateFilters(GenericAPIView):
    """
    A class-based view for handling GET requests with filters.

    Attributes:
        filter_backends (tuple): The filter backends to be used.
        pagination_class (class): The pagination class to be used.
        page_size_query_param (str): The query parameter for specifying the page size.
        ordering_fields (list): The fields that can be used for ordering.
        permission_classes (list): The permission classes required for accessing the view.

    """

    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    pagination_class = StandardResultsSetPagination
    page_size_query_param = "page_size"
    ordering_fields = ["created_at", "updated_at"]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET requests.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response object.

        Raises:
            ValueError: If there is an error in the filterset.

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
