from django_filters import rest_framework as filters


class BaseFilterStatus(filters.FilterSet):
    status = filters.CharFilter(field_name="status", method="filter_status")

    def filter_status(self, qs, _, value):
        """
        Filters the queryset by the start date.

        Args:
            qs: The queryset to filter.
            name: The name of the filter. Not used in this method but required by the base class.
            value: The value of the start date filter.

        Returns:
            QuerySet: The filtered queryset.
        """
        value = value.split(",")
        return qs.filter(status__in=value)
