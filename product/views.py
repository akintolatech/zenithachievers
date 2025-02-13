from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product




def product_page (request):
    products = Product.objects.all()
    context = {
        'products': products,
        'products_count': products.count()
    }
    return render(request, 'productreview/productreview.html', context)

def whatsapp_page (request):
    # products = Product.objects.all()
    context = {
        # 'products': products,
        # 'products_count': products.count()
    }
    return render(request, 'whatsapp/whatsapp.html', context)


def contact_page (request):
    # products = Product.objects.all()
    context = {
        # 'products': products,s
        # 'products_count': products.count()
    }
    return render(request, 'contactadmin/contactadmin.html', context)

def whatsapp_withdrawal_page (request):
    # products = Product.objects.all()
    context = {
        # 'products': products,
        # 'products_count': products.count()
    }
    return render(request, 'whatsappwithdrawals/whatsappwithdrawals.html', context)


def loans_page (request):
    # products = Product.objects.all()
    context = {
        # 'products': products,
        # 'products_count': products.count()
    }
    return render(request, 'loan/loan.html', context)

# def transfer (request):
#     # products = Product.objects.all()
#     context = {
#         # 'products': products,
#         # 'products_count': products.count()
#     }
#     return render(request, 'finance/transfer.html', context)
#
# def withdrawal (request):
#     # products = Product.objects.all()
#     context = {
#         # 'products': products,
#         # 'products_count': products.count()
#     }
#     return render(request, 'finance/withdrawal.html', context)
#
# def redeem_points (request):
#     # products = Product.objects.all()
#     context = {
#         # 'products': products,
#         # 'products_count': products.count()
#     }
#     return render(request, 'finance/redeempoint.html', context)
#
# def mini_statements (request):
#     # products = Product.objects.all()
#     context = {
#         # 'products': products,
#         # 'products_count': products.count()
#     }
#     return render(request, 'finance/ministatements.html', context)