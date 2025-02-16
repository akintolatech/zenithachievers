from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = "administration"
urlpatterns = [
    # Add patterns here
    path('', views.administration_dashboard, name='administration'),
    path('fetch_orders/', views.fetch_orders, name='fetch_orders'),

]