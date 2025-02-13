from django.shortcuts import render

# Create your views here.
def transfer (request):
    # products = Product.objects.all()
    context = {
        # 'products': products,
        # 'products_count': products.count()
    }
    return render(request, 'finance/transfer.html', context)

def withdrawal (request):
    # products = Product.objects.all()
    context = {
        # 'products': products,
        # 'products_count': products.count()
    }
    return render(request, 'finance/withdrawal.html', context)

def redeem_points (request):
    # products = Product.objects.all()
    context = {
        # 'products': products,
        # 'products_count': products.count()
    }
    return render(request, 'finance/redeempoint.html',)

def mini_statements (request):
    # products = Product.objects.all()
    context = {
        # 'products': products,
        # 'products_count': products.count()
    }
    return render(request, 'finance/ministatements.html', context)