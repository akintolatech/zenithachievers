from deposit.models import Deposit
from finance.models import Withdraw, Transfer
# from .forms import EditProductForm, ProductForm
from django.urls import reverse

from django.db.models.functions import TruncDate
from django.db.models import Count, Sum
from datetime import date, timedelta
from django.shortcuts import render


from django.shortcuts import render
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

# def administration_dashboard(request):
#     today = date.today()
#     last_30_days = [today - timedelta(days=i) for i in range(7)]
#
#     deposits = (
#         Deposit.objects.filter(created__gte=min(last_30_days))
#         .annotate(day=TruncDate("created"))
#         .values("day")
#         .annotate(count=Count("id"))
#     )
#
#     withdrawals = (
#         Withdraw.objects.filter(created__gte=min(last_30_days))
#         .annotate(day=TruncDate("created"))
#         .values("day")
#         .annotate(count=Count("id"))
#     )
#
#     transfers = (
#         Transfer.objects.filter(created__gte=min(last_30_days))
#         .annotate(day=TruncDate("created"))
#         .values("day")
#         .annotate(count=Count("id"))
#     )
#
#     deposit_counts = {entry["day"].strftime("%Y-%m-%d"): entry["count"] for entry in deposits}
#     withdrawal_counts = {entry["day"].strftime("%Y-%m-%d"): entry["count"] for entry in withdrawals}
#     transfer_counts = {entry["day"].strftime("%Y-%m-%d"): entry["count"] for entry in transfers}
#
#     days = [day.strftime("%Y-%m-%d") for day in reversed(last_30_days)]
#     daily_deposits = [deposit_counts.get(day, 0) for day in days]
#     daily_withdrawals = [withdrawal_counts.get(day, 0) for day in days]
#     daily_transfers = [transfer_counts.get(day, 0) for day in days]
#
#     context = {
#         "total_deposits": Deposit.objects.count(),
#         "total_withdrawals": Withdraw.objects.count(),
#         "total_transfer": Transfer.objects.count(),
#         "days": json.dumps(days),
#         "daily_deposits": json.dumps(daily_deposits),
#         "daily_withdrawals": json.dumps(daily_withdrawals),
#         "daily_transfers": json.dumps(daily_transfers),
#     }
#
#     return render(request, "administration/administration_dashboard.html", context)


