from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Package, UserPackage


# @login_required
# def purchase_package(request, package_id):
#     package = get_object_or_404(Package, id=package_id)
#
#     # Check if user already purchased this package
#     if UserPackage.objects.filter(user=request.user, package=package).exists():
#         return redirect('dashboard')  # Redirect if already purchased
#
#     UserPackage.objects.create(user=request.user, package=package)
#     return redirect('dashboard')  # Redirect to dashboard after purchase


def package_list (request):
    packages = Package.objects.all()
    context = {
        'packages': packages,
        'packages_count': packages.count()
    }
    return render(request, 'Packages/Packages.html', context)
