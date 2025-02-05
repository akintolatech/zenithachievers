from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views


urlpatterns = [
    # path('', views.landing, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),

]