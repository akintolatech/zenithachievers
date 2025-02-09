from django.urls import path
from . import views


app_name = "whatsapp"

urlpatterns = [
    path('submit_whatsapp_screenshot/', views.submit_whatsapp_screenshot, name='submit_whatsapp_screenshot'),
    path('make_whatsapp_withdrawal/', views.make_whatsapp_withdrawal, name='make_whatsapp_withdrawal'),
]