from django.urls import path
from . import views


app_name = "finance"

urlpatterns = [

    path('transfer/', views.make_transfer, name='make_transfer'),
    path('withdrawal/', views.withdrawal, name='withdrawal'),
    path('redeem_points/', views.redeem_points, name='redeem_points'),
    path('mini_statements/', views.mini_statements, name='mini_statements'),

]