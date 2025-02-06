from django.urls import path
from . import views

app_name = "deposits"

urlpatterns = [
    path('', views.deposit_page, name='deposit'),
]