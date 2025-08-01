from django.urls import path
from . import views

app_name = "deposits"

urlpatterns = [
    path('make_deposit/', views.deposit_page, name='make_deposit'),

    # MPESA_API's
    path('ajax/', views.ajax_deposit, name='ajax_deposit'),  # new AJAX endpoint
    path('status/<str:checkout_id>/', views.stk_status, name='stk_status'),
    # path("daraja_stk_push/", views.daraja_stk_push, name="daraja_stk_push"),
    # path('mpesa/stk-callback/', views.stk_callback, name='stk_callback'),
]