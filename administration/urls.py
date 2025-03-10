from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = "administration"

urlpatterns = [
    # Add patterns here
    path('', views.administration_dashboard, name='administration'),

    # Users
    path('users/', views.users, name='users'),
    path('user_details/<int:user_id>/', views.user_details, name='user_details'),
    path('active_users/', views.active_users, name='active_users'),
    path('dormant_users/', views.dormant_users, name='dormant_users'),

    # Deposits
    path('user_deposits/', views.user_deposits, name='user_deposits'),
    path('approved_user_deposits/', views.approved_deposits, name='approved_user_deposits'),
    path('un_approved_user_deposits/', views.un_approved_deposits, name='un_approved_user_deposits'),
    path('deposits/<str:deposit_id>/', views.deposit_action, name='deposit_action'),

    # Withdraws
    path('user_withdraws/', views.user_withdraws, name='user_withdraws'),
    path('withdraws/<str:withdraw_id>/', views.withdraw_action, name='withdraw_action'),
    path('approved_user_withdraws/', views.approved_withdraws, name='approved_user_withdraws'),
    path('un_approved_user_withdraws/', views.un_approved_withdraws, name='un_approved_user_withdraws'),

    #  Whatsapp
    path('user_whatsapp_screenshots/', views.user_whatsapp_screenshots, name='user_whatsapp_screenshots'),
    path('whatsapp_screenshot/<str:whatsapp_screenshot_id>/', views.whatsapp_screenshot_action, name='whatsapp_screenshot_action'),
    path('approved_whatsapp_screenshots/', views.approved_whatsapp_screenshots, name='approved_whatsapp_screenshots'),
    path('un_approved_whatsapp_screenshots/', views.un_approved_whatsapp_screenshots, name='un_approved_whatsapp_screenshots'),
]