
from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('all_referrals/', views.all_referrals, name='all_referrals'),
    path('basic_referrals/', views.basic_referrals, name='basic_referrals'),
    path('premium_referrals/', views.premium_referrals, name='premium_referrals'),
    path('gold_referrals/', views.gold_referrals, name='gold_referrals'),
    path('dormant_referrals/', views.dormant_referrals, name='dormant_referrals'),

]