from deposit.models import Deposit
from finance.models import Withdraw, Transfer
# from .forms import EditProductForm, ProductForm
from django.urls import reverse
from account.models import Profile
from django.db.models.functions import TruncDate
from django.db.models import Count, Sum
from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from deposit.models import Deposit
from django.shortcuts import render
from .forms import DepositApprovalForm
import json

def administration_dashboard(request):
    today = date.today()
    last_30_days = [today - timedelta(days=i) for i in range(7)]  # Fetch data for last 7 days

    # Fetching counts per day
    deposits = (
        Deposit.objects.filter(created__gte=min(last_30_days))
        .annotate(day=TruncDate("created"))
        .values("day")
        .annotate(count=Count("id"))
    )

    withdrawals = (
        Withdraw.objects.filter(created__gte=min(last_30_days))
        .annotate(day=TruncDate("created"))
        .values("day")
        .annotate(count=Count("id"))
    )

    transfers = (
        Transfer.objects.filter(created__gte=min(last_30_days))
        .annotate(day=TruncDate("created"))
        .values("day")
        .annotate(count=Count("id"))
    )

    # Convert counts to dictionaries
    deposit_counts = {entry["day"].strftime("%Y-%m-%d"): entry["count"] for entry in deposits}
    withdrawal_counts = {entry["day"].strftime("%Y-%m-%d"): entry["count"] for entry in withdrawals}
    transfer_counts = {entry["day"].strftime("%Y-%m-%d"): entry["count"] for entry in transfers}

    days = [day.strftime("%Y-%m-%d") for day in reversed(last_30_days)]
    daily_deposits = [deposit_counts.get(day, 0) for day in days]
    daily_withdrawals = [withdrawal_counts.get(day, 0) for day in days]
    daily_transfers = [transfer_counts.get(day, 0) for day in days]

    # Compute total sums
    total_deposit_amount = Deposit.objects.aggregate(total=Sum("amount"))["total"] or 0
    total_withdraw_amount = Withdraw.objects.aggregate(total=Sum("amount"))["total"] or 0
    total_transfer_amount = Transfer.objects.aggregate(total=Sum("amount"))["total"] or 0

    context = {
        "total_deposits": Deposit.objects.count(),
        "total_withdrawals": Withdraw.objects.count(),
        "total_transfer": Transfer.objects.count(),
        "total_deposit_amount": total_deposit_amount,  # Total sum of deposits
        "total_withdraw_amount": total_withdraw_amount,  # Total sum of withdrawals
        "total_transfer_amount": total_transfer_amount,  # Total sum of transfers
        "days": json.dumps(days),
        "daily_deposits": json.dumps(daily_deposits),
        "daily_withdrawals": json.dumps(daily_withdrawals),
        "daily_transfers": json.dumps(daily_transfers),
    }

    return render(request, "administration/administration_dashboard.html", context)


# Users
def users(request):


    context = {
        "total_users": Profile.objects.count(),
        "profiles": Profile.objects.all(),
        "total_active_users": Profile.objects.filter(account_status=Profile.AccountStatus.ACTIVE).count(),
        "total_dormant_users": Profile.objects.filter(account_status=Profile.AccountStatus.DORMANT).count(),
        "active_users": active_users,
        "dormant_users": dormant_users,
    }
    return render(request, "administration/users/admin_users.html", context)


def active_users(request):

    active_users_list = Profile.objects.filter(account_status=Profile.AccountStatus.ACTIVE)

    context = {
        "active_users_list": active_users_list,
    }
    return render(request, "administration/users/active_users.html", context)


def dormant_users(request):

    dormant_users_list = Profile.objects.filter(account_status=Profile.AccountStatus.DORMANT)

    context = {
        "dormant_users_list": dormant_users_list,
    }
    return render(request, "administration/users/dormant_users.html", context)


# Deposits
def user_deposits(request):

    context = {
        "all_user_deposits": Deposit.objects.all(),
        "total_user_deposits": Deposit.objects.all().count(),
        "approved_user_deposits": Deposit.objects.filter(paid=True).count(),
        "un_approved_user_deposits": Deposit.objects.filter(paid=False).count(),
    }

    return render(request, "administration/deposits/user_deposits.html", context)


def deposit_action(request, deposit_id):
    deposit_request = get_object_or_404(Deposit, reference_code=deposit_id)

    if request.method == "POST":
        form = DepositApprovalForm(request.POST, instance=deposit_request)
        if form.is_valid():
            form.save()  # This will trigger the save method in the model
            return redirect('administration:user_deposits')  # Change 'deposit_list' to your actual view

    else:
        form = DepositApprovalForm(instance=deposit_request)

    context = {
        "form": form,
        "deposit_request": deposit_request
    }

    return render(request, "administration/deposits/approve_deposit.html", context)


def approved_deposits(request):

    context = {
        "approved_user_deposits": Deposit.objects.filter(paid=True),
    }

    return render(request, "administration/deposits/approved_user_deposits.html", context)


def un_approved_deposits(request):

    context = {
        "un_approved_user_deposits": Deposit.objects.filter(paid=False),
    }

    return render(request, "administration/deposits/unapproved_user_deposits.html", context)


# Withdrawal
def user_withdrawals(request):

    context = {
        "all_user_deposits": Deposit.objects.all(),
        "total_user_deposits": Deposit.objects.all().count(),
        "approved_user_deposits": Deposit.objects.filter(paid=True).count(),
        "un_approved_user_deposits": Deposit.objects.filter(paid=False).count(),
    }

    return render(request, "administration/deposits/user_deposits.html", context)


# def deposit_action(request, deposit_id):
#     deposit_request = get_object_or_404(Deposit, reference_code=deposit_id)
#
#     if request.method == "POST":
#         form = DepositApprovalForm(request.POST, instance=deposit_request)
#         if form.is_valid():
#             form.save()  # This will trigger the save method in the model
#             return redirect('administration:user_deposits')  # Change 'deposit_list' to your actual view
#
#     else:
#         form = DepositApprovalForm(instance=deposit_request)
#
#     context = {
#         "form": form,
#         "deposit_request": deposit_request
#     }
#
#     return render(request, "administration/deposits/approve_deposit.html", context)
#
#
# def approved_deposits(request):
#
#     context = {
#         "approved_user_deposits": Deposit.objects.filter(paid=True),
#     }
#
#     return render(request, "administration/deposits/approved_user_deposits.html", context)
#
#
# def un_approved_deposits(request):
#
#     context = {
#         "un_approved_user_deposits": Deposit.objects.filter(paid=False),
#     }
#
#     return render(request, "administration/deposits/unapproved_user_deposits.html", context)
#
#
