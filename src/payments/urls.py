"""Appointments URLs."""

from django.urls import path

from payments.views import PaymentView

app_name = "payments"  # pylint: disable=C0103

urlpatterns = [
    path("", PaymentView.as_view(), name="payment"),
]
