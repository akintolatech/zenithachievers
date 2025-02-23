from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = "administration"

urlpatterns = [
    # Add patterns here
    path('', views.administration_dashboard, name='administration'),
    path('users/', views.users, name='users'),
    path('active_users/', views.active_users, name='active_users'),
    path('dormant_users/', views.dormant_users, name='dormant_users'),
    path('user_deposits/', views.user_deposits, name='user_deposits'),
    path('approved_user_deposits/', views.approved_deposits, name='approved_user_deposits'),
    path('un_approved_user_deposits/', views.un_approved_deposits, name='un_approved_user_deposits'),
    path('deposits/<str:deposit_id>/', views.deposit_action, name='deposit_action'),
]