import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from daraja_api.core import MpesaClient
from daraja_api.exceptions import MpesaConnectionError
from .forms import DepositForm
from django.contrib import messages
from .models import Deposit
from django.http import HttpResponse, JsonResponse



@login_required
def deposit_page(request):
    user_deposits = Deposit.objects.filter(user=request.user)

    if request.method == "POST":
        deposit_form = DepositForm(request.POST)
        if deposit_form.is_valid():

            if deposit_form.cleaned_data["amount"] < 100:
                messages.error(request, "Please Deposit more than 100")
                return redirect("deposits:make_deposit")


            deposit = deposit_form.save(commit=False)
            deposit.user = request.user  # Assign the user

            deposit.save()
            messages.success(request, "Your deposit has been successfully Placed - Your Deposit will reflect on your dashboard after confirmed by Admin!")
            return redirect('deposits:make_deposit')  # Redirect to prevent form resubmission

    else:
        deposit_form = DepositForm()

    context = {
        'user_deposits': user_deposits,
        'user_deposits_count': user_deposits.count(),
        "deposit_form": deposit_form
    }
    return render(request, 'Deposit/deposit.html', context)


def daraja_stk_push(request):
    try:
        cl = MpesaClient()
        # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
        phone_number = '0708374149'
        amount = 100
        account_reference = 'ZenithAchievers'
        transaction_desc = 'Description'
        callback_url = 'http://zenithachievers.com/mpesa/stk-callback/'
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        print(response)
        return HttpResponse(response)

    except Exception as e:
        messages.error(request, f"An Error Occurred... {e}.")
        return redirect('deposits:make_deposit')



@csrf_exempt
def stk_callback(request):
    if request.method == 'POST':
        mpesa_response = json.loads(request.body)
        print("M-Pesa Callback:", mpesa_response)

        # You can now save the payment status, phone, transaction code, etc.
        # Example: result_code = mpesa_response['Body']['stkCallback']['ResultCode']

        return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})
    return JsonResponse({"error": "Invalid request"}, status=400)

# @login_required
# def stk_status(request, checkout_id):
#     stk = get_object_or_404(StkPushRequest, checkout_request_id=checkout_id, user=request.user)
#     return JsonResponse({"status": stk.status, "result_desc": stk.result_desc})