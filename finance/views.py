from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from .forms import TransferForm, WithdrawalForm
from .models import Transfer, Withdraw
from django.contrib import messages
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from account.models import Profile
from decimal import Decimal
from itertools import chain

@login_required
def make_transfer(request):
    transfer_history = Transfer.objects.filter(sender=request.user)  # Fetch user's transfer history

    if request.method == 'POST':
        transfer_form = TransferForm(request.POST)
        if transfer_form.is_valid():
            transfer = transfer_form.save(commit=False)
            sender_profile = request.user.profile

            # Validate transfer amount
            if transfer.amount <= 0:
                messages.error(request, "Transfer amount must be greater than zero.")
                return redirect('finance:make_transfer')

            if transfer.amount > 130:
                messages.error(request, "Transfer amount cannot be greater than 130")
                return redirect('finance:make_transfer')

            if transfer.amount > sender_profile.deposit_balance:
                messages.error(request, "Insufficient Deposit balance!")
                return redirect('finance:make_transfer')

            # Validate receiver
            try:
                receiver_user = User.objects.get(username=transfer.receiver)

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

            # ✅ Assign sender before saving to avoid NULL constraint errors
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


@login_required
def withdrawal(request):
    """Handles user withdrawal requests."""
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found. Please contact support.")
        return redirect("finance:withdrawal")

    if request.method == "POST":
        withdrawal_form = WithdrawalForm(request.POST)
        if withdrawal_form.is_valid():
            withdrawal_amount = Decimal(withdrawal_form.cleaned_data["amount"])
            withdrawal_charges = withdrawal_amount * Decimal("0.05")
            total_withdrawal_amount = withdrawal_amount + withdrawal_charges

            # Validate withdrawal amount
            if total_withdrawal_amount <= 0:
                messages.error(request, "Invalid withdrawal amount.")
                return redirect("finance:withdrawal")

            if total_withdrawal_amount > profile.earning_balance:
                messages.error(request, "Insufficient funds for withdrawal.")
                return redirect("finance:withdrawal")

            # Perform withdrawal within a database transaction
            # try:
            with transaction.atomic():
                # Deduct balance
                profile.earning_balance -= total_withdrawal_amount
                profile.save()

                # Save withdrawal record
                withdraw = withdrawal_form.save(commit=False)
                withdraw.user = request.user
                withdraw.charge = withdrawal_charges  # Save the 5% charge
                withdraw.save()

            messages.success(request, "Withdrawal request submitted successfully.")
            return redirect("finance:withdrawal")

            # except Exception as e:
            #     # logger.error(f"Withdrawal error for user {request.user.username}: {e}")
            #     messages.error(request, f"An error occurred ({e}) while processing your withdrawal. Please try again.")
            #     return redirect("finance:withdrawal")

    else:
        withdrawal_form = WithdrawalForm()

    # Fetch user's withdrawal history
    withdrawal_history = Withdraw.objects.filter(user=request.user).order_by("-created")

    context = {
        "withdrawal_form": withdrawal_form,
        "withdrawal_history": withdrawal_history,
    }
    return render(request, "finance/withdrawal.html", context)



def redeem_points (request):
    # products = Product.objects.all()
    context = {
        # 'products': products,
        # 'products_count': products.count()
    }
    return render(request, 'finance/redeempoint.html',)


def mini_statements(request):
    transfers = Transfer.objects.filter(sender=request.user).order_by('-created')
    withdrawals = Withdraw.objects.filter(user=request.user).order_by('-created')

    # Merge and sort by created timestamp
    transactions = sorted(
        chain(transfers, withdrawals),
        key=lambda x: x.created,
        reverse=True
    )

    context = {
        'transactions': transactions,
    }

    return render(request, 'finance/ministatements.html', context)