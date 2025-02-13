from django.urls import path
from . import views


app_name = "finance"

urlpatterns = [

    path('transfer/', views.transfer, name='transfer'),

]