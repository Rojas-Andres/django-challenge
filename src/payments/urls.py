"""Appointments URLs."""

from django.urls import path

from payments.views import PaymentStatusView, PaymentView

app_name = "payments"  # pylint: disable=C0103

urlpatterns = [
    path("", PaymentView.as_view(), name="payment"),
    path("status/", PaymentStatusView.as_view(), name="payment_status"),
]
