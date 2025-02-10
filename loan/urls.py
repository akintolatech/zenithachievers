from django.urls import path
from . import views

app_name = "loan"

urlpatterns = [
    path('make_loan_request/', views.make_loan_request, name='make_loan_request'),
]