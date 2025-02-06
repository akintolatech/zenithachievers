from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def deposit_page (request):

    context = {
        # 'packages': packages,
        # 'packages_count': packages.count()
    }

    return render(request, 'Deposit/deposit.html', context)
