
from django.urls import path
from . import views

app_name = "package"

urlpatterns = [
    path('purchase/<int:package_id>/', views.purchase_package, name='purchase_package'),
    path('packages/', views.package_list, name='packages'),
]