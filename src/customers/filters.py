from datetime import datetime

import pytz  # type: ignore
from django_filters import rest_framework as filters

from customers.models import Customer
from utils.filters import BaseFilterStatus


class BaseDateFilterSet(filters.FilterSet):
    """
    A base filter set for filtering by date.

    This filter set provides methods for filtering a queryset based on a start date and end date.

    Attributes:
        preapproved_at (CharFilter): A filter for the start date.
        preapproved_at_less (CharFilter): A filter for the end date.
    """

    preapproved_at = filters.CharFilter(method="filter_preapproved_at")
    preapproved_at_less = filters.CharFilter(method="filter_preapproved_less")

    def filter_preapproved_at(self, qs, _, value):
        """
        Filters the queryset by the start date.

        Args:
            qs (QuerySet): The queryset to filter.
            name (str): The name of the filter. Not used in this method but required by the base class.
            value (str): The value of the start date filter.

        Returns:
            QuerySet: The filtered queryset.
        """
        preapproved_at = datetime.strptime(value, "%Y-%m-%d")
        start = datetime.combine(preapproved_at, datetime.min.time()).astimezone(pytz.UTC)
        return qs.filter(preapproved_at__gte=start)

    def filter_preapproved_less(self, qs, _, value):
        """
        Filters the queryset by the end date.

        Args:
            qs (QuerySet): The queryset to filter.
            name (str): The name of the filter. Not used in this method but required by the base class.
            value (str): The value of the end date filter.

        Returns:
            QuerySet: The filtered queryset.
        """
        preapproved_at = datetime.strptime(value, "%Y-%m-%d")
        start = datetime.combine(preapproved_at, datetime.min.time()).astimezone(pytz.UTC)
        return qs.filter(preapproved_at__lt=start)


class CustomerFilters(BaseDateFilterSet, BaseFilterStatus):
    external_id = filters.CharFilter(field_name="external_id", lookup_expr="icontains")

    class Meta:
        model = Customer
        fields: list[str] = ("external_id", "status", "created_at")
