from django_filters import rest_framework as filters

from loans.models import Loan
from utils.filters import BaseFilterStatus


class LoanFilters(BaseFilterStatus):
    external_id = filters.CharFilter(field_name="external_id", lookup_expr="icontains")
    customer_external_id = filters.CharFilter(field_name="customer__external_id", lookup_expr="icontains")

    class Meta:
        model = Loan
        fields: list[str] = ("external_id", "status", "contract_version", "customer_external_id")
