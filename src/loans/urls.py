"""Appointments URLs."""

from django.urls import path

from loans.views import LoanView, LoanStatusLoan

app_name = "loans"  # pylint: disable=C0103

urlpatterns = [
    path("", LoanView.as_view(), name="loan"),
    path("status/", LoanStatusLoan.as_view(), name="loan_status"),
]
