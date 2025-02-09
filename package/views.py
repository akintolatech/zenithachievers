from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Package, UserPackage
from account.models import Profile


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

@login_required
def package_list (request):
    packages = Package.objects.all()
    user_packages = UserPackage.objects.filter(user=request.user)
    context = {
        'packages': packages,
        'packages_count': packages.count(),
        "user_packages": user_packages
    }
    return render(request, 'Packages/Packages.html', context)


@login_required
def purchase_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    profile = Profile.objects.get(user=request.user)

    # Check if user already purchased this package
    if UserPackage.objects.filter(user=request.user, package=package).exists():
        messages.error(request, "You have already purchased this package.")
        return redirect('package:packages')

    # Check if deposit balance is sufficient
    if profile.deposit_balance < package.price:
        messages.error(request, "Insufficient deposit balance. Please top up.")
        return redirect('package:packages')

    # Deduct package price from deposit balance
    profile.deposit_balance -= package.price
    profile.save()

    # Create UserPackage record
    UserPackage.objects.create(user=request.user, package=package)

    # Activate account if it's dormant
    if profile.account_status == Profile.AccountStatus.DORMANT:
        profile.activate_account()

    messages.success(request, "Package purchased successfully!")
    return redirect('package:packages')