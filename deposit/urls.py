from django.urls import path
from . import views

app_name = "deposits"

urlpatterns = [
    path('make_deposit', views.deposit_page, name='make_deposit'),
]