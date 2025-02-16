from django.http import JsonResponse
from django.shortcuts import render, redirect
from orders.models import Order
from shop.models import Product
from account.models import Profile
from .forms import EditProductForm, ProductForm
from django.urls import reverse



# Create your views here.
def administration_dashboard(request):
    total_orders = Order.objects.all()
    products = Product.objects.all()
    total_profiles = Profile.objects.all()

    edit_product_form = EditProductForm()
    product_form = ProductForm()

    context = {
        "total_orders": total_orders.count(),
        "total_products": products.count(),
        "total_profiles": total_profiles.count(),
        "products": products,
        "product_form": product_form
    }

    return render( request, "administration/administration_dashboard.html", context)


def fetch_orders(request):
    total_orders = Order.objects.all()

    # Data for all logs
    total_orders_data = [
        {"counter": idx + 1, "details": order.email, "created": order.created.strftime('%Y-%m-%d %H:%M:%S')}
        for idx, order in enumerate(total_orders)
    ]

    return JsonResponse(
        {
            # "recent_logs": recent_log_data,
            "all_orders": total_orders_data
        },
        safe=False
    )

# def edit_product(request):
#     if request.method == "POST":
#         edit_product_form = EditProductForm(
#             instance=request.user,
#             data=request.POST
#         )
#
#         if edit_product_form.is_valid() :
#             edit_product_form.save()
#     else:
#         edit_product_form = EditProductForm(instance=request.user)
#
#     return render(
#         request,
#         'authenticator/edit-student.html',
#         {
#             'edit_product_form': edit_product_form,
#         }
#     )
#
#
# def create_product(request):
#     if request.method == "POST":
#         product_form = ProductForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return redirect(reverse("administration_dashboard"))  # Redirect to the dashboard after creation
#     else:
#         product_form = ProductForm()
#
#     return render(request, "administration/create_product.html", {"product_form": product_form})
