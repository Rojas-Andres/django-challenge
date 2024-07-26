"""Appointments URLs."""

from django.urls import path

from customers.views import CustomerView

app_name = "customers"  # pylint: disable=C0103

urlpatterns = [
    path("", CustomerView.as_view(), name="customer"),
]
