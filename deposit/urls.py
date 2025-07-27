from django.urls import path
from . import views

app_name = "deposits"

urlpatterns = [
    path('make_deposit', views.deposit_page, name='make_deposit'),

    # MPESA_API's
    path("mpesa/stkpush/", views.initiate_stk_push, name="stkpush"),
    path("mpesa/callback/", views.stk_callback, name="stk_callback"),
    path("mpesa/status/<str:checkout_id>/", views.stk_status, name="stk_status"),
]