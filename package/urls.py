
from django.urls import path
from . import views

app_name = "package"

urlpatterns = [
    path('packages/', views.package_list, name='packages'),
]