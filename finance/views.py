from django.contrib.auth.models import User
from django.db.transaction import commit
from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import TransferForm
from .models import Transfer
from django.contrib import messages
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from account.models import Profile


def make_transfer(request):
    transfer_history = Transfer.objects.filter(sender=request.user)
    if request.method == 'POST':
        transfer_form = TransferForm(request.POST)
        if transfer_form.is_valid():
            transfer = transfer_form.save(commit=False)
            sender_profile = request.user.profile  # Access sender's profile

            # Check if the amount is valid
            if transfer.amount <= 0:
                messages.error(request, "Transfer amount must be greater than zero.")
                return redirect('finance:make_transfer')

            # Check if amount is within 130
            if transfer.amount > 130:
                messages.error(request, "Transfer amount cannot be greater than 130")
                return redirect('finance:make_transfer')

            # Check if sender has enough balance
            if transfer.amount > sender_profile.deposit_balance:
                messages.error(request, "Insufficient Deposit balance!")
                return redirect('finance:make_transfer')

            # Validate receiver
            try:
                receiver_user = User.objects.get(username=transfer.receiver)

                # Prevent self-transfer
                if receiver_user == request.user:
                    messages.error(request, "You cannot transfer funds to yourself!")
                    return redirect('finance:make_transfer')

            except User.DoesNotExist:
                messages.error(request, "Receiver username is invalid!")
                return redirect('finance:make_transfer')

            # Update sender's balance
            sender_profile.deposit_balance -= transfer.amount
            sender_profile.save()

            # Update receiver's balance
            receiver_profile = receiver_user.profile
            receiver_profile.deposit_balance += transfer.amount
            receiver_profile.save()

            # Save transfer details
            transfer.sender = request.user
            transfer.save()

            messages.success(request,
                             f"Your Transfer of {transfer.amount} to {receiver_user.username} has been successfully made.")
            return redirect('finance:make_transfer')

    else:
        transfer_form = TransferForm()

    context = {
        "transfer_form": transfer_form,
        "transfer_history": transfer_history
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