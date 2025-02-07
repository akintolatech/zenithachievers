
from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('loans/', views.loans_page, name='loans'),
    path('whatsapp_withdrawals/', views.whatsapp_withdrawal_page, name='whatsapp_withdrawals'),
    path('contact_admin/', views.contact_page, name='contact_admin'),
    path('whatsapp/', views.whatsapp_page, name='whatsapp'),
    path('product_view/', views.product_page, name='product_view'),
]