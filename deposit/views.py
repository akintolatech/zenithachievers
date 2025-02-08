from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Deposit
from .forms import DepositForm
from django.contrib import messages

@login_required
def deposit_page(request):
    user_deposits = Deposit.objects.filter(user=request.user)

    if request.method == "POST":
        deposit_form = DepositForm(request.POST)
        if deposit_form.is_valid():
            deposit = deposit_form.save(commit=False)
            deposit.user = request.user  # Assign the user
            deposit.save()
            messages.success(request, "Your deposit has been successfully made!")
            return redirect('deposits:make_deposit')  # Redirect to prevent form resubmission

    else:
        deposit_form = DepositForm()

    context = {
        'user_deposits': user_deposits,
        'user_deposits_count': user_deposits.count(),
        "deposit_form": deposit_form
    }
    return render(request, 'Deposit/deposit.html', context)