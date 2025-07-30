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



# @login_required
# def deposit_page(request):
#     user_deposits = Deposit.objects.filter(user=request.user)
#
#     if request.method == "POST":
#         deposit_form = DepositForm(request.POST)
#         if deposit_form.is_valid():
#
#             if deposit_form.cleaned_data["amount"] < 100:
#                 messages.error(request, "Please Deposit more than 100")
#                 return redirect("deposits:make_deposit")
#
#
#             deposit = deposit_form.save(commit=False)
#             deposit.user = request.user  # Assign the user
#
#             deposit.save()
#             messages.success(request, "Your deposit has been successfully Placed - Your Deposit will reflect on your dashboard after confirmed by Admin!")
#             return redirect('deposits:make_deposit')  # Redirect to prevent form resubmission
#
#     else:
#         deposit_form = DepositForm()
#
#     context = {
#         'user_deposits': user_deposits,
#         'user_deposits_count': user_deposits.count(),
#         "deposit_form": deposit_form
#     }
#     return render(request, 'Deposit/deposit.html', context)

@login_required
def deposit_page(request):
    user_deposits = Deposit.objects.filter(user=request.user)
    deposit_form = DepositForm()

    context = {
        'user_deposits': user_deposits,
        'user_deposits_count': user_deposits.count(),
        'deposit_form': deposit_form,
    }
    return render(request, 'Deposit/deposit.html', context)


@login_required
@csrf_exempt  # Optional if you handle CSRF via fetch headers correctly
@csrf_exempt
@login_required
def ajax_deposit(request):
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "Only POST requests allowed"}, status=405)

    form = DepositForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"ok": False, "error": "Invalid form data"})

    amount = form.cleaned_data["amount"]
    if amount < 100:
        return JsonResponse({"ok": False, "error": "Please deposit more than 100."})

    deposit = form.save(commit=False)
    deposit.user = request.user
    deposit.paid = False
    deposit.save()

    try:
        cl = MpesaClient()
        phone = deposit.phone_number
        account_reference = 'ZenithAchievers'
        transaction_desc = f'Deposit: {deposit.reference_code}'
        callback_url = 'https://zenithachievers.com/mpesa/stk-callback/'

        response = cl.stk_push(phone, amount, account_reference, transaction_desc, callback_url)
        response_data = response.json() if hasattr(response, 'json') else response
        print("M-PESA API Response:", response_data)

        # Handle API failure
        if response_data.get("ResponseCode") != "0":
            return JsonResponse({
                "ok": False,
                "error": response_data.get("errorMessage")
                         or response_data.get("ResponseDescription")
                         or "Unknown error from M-PESA"
            })

        # Save checkout ID if available
        checkout_id = response_data.get("CheckoutRequestID")
        if checkout_id:
            deposit.checkout_request_id = checkout_id
            deposit.save()

        return JsonResponse({
            "ok": True,
            "message": response_data.get("CustomerMessage", "STK Push sent successfully."),
            "checkout_request_id": checkout_id
        })

    except Exception as e:
        return JsonResponse({
            "ok": False,
            "error": f"Failed to initiate STK Push: {str(e)}"
        })









# def ajax_deposit(request):
#     if request.method != "POST":
#         return JsonResponse({"ok": False, "error": "Only POST requests allowed"}, status=405)
#
#     form = DepositForm(request.POST)
#     if not form.is_valid():
#         return JsonResponse({"ok": False, "error": "Invalid form data"})
#
#     amount = form.cleaned_data["amount"]
#     if amount < 100:
#         return JsonResponse({"ok": False, "error": "Please deposit more than 100."})
#
#     deposit = form.save(commit=False)
#     deposit.user = request.user
#     deposit.paid = False
#     deposit.save()
#
#     try:
#         cl = MpesaClient()
#         phone = '0705862990'
#         account_reference = 'ZenithAchievers'
#         transaction_desc = f'Deposit: {deposit.reference_code}'
#         callback_url = 'http://zenithachievers.com/mpesa/stk-callback/'
#
#         response = cl.stk_push(phone, amount, account_reference, transaction_desc, callback_url)
#         response_data = response.json() if hasattr(response, 'json') else response
#         print(response_data)
#
#         checkout_id = response_data.get("CheckoutRequestID")
#         if checkout_id:
#             deposit.checkout_request_id = checkout_id
#             deposit.save()
#
#         return JsonResponse({
#             "ok": True,
#             "message": f"STK Push sent to {deposit.phone_number}",
#             "checkout_request_id": checkout_id
#         })
#
#     except Exception as e:
#         return JsonResponse({
#             "ok": False,
#             "error": f"Failed to initiate STK Push: {str(e)}"
#         })

#@login_required
# def deposit_page(request):
#     user_deposits = Deposit.objects.filter(user=request.user)
#
#     if request.method == "POST":
#         deposit_form = DepositForm(request.POST)
#
#         if not deposit_form.is_valid():
#             messages.error(request, "Please correct the errors below.")
#             return redirect("deposits:make_deposit")
#
#         amount = deposit_form.cleaned_data["amount"]
#         if amount < 100:
#             messages.error(request, "Please deposit more than 100.")
#             return redirect("deposits:make_deposit")
#
#         # Save deposit object (unpaid)
#         deposit = deposit_form.save(commit=False)
#         deposit.user = request.user
#         deposit.paid = False
#         deposit.save()
#
#         try:
#             # Initiate STK Push
#             cl = MpesaClient()
#             phone = deposit.phone_number
#             account_reference = 'ZenithAchievers'
#             transaction_desc = f'Deposit: {deposit.reference_code}'
#             callback_url = 'http://zenithachievers.com/mpesa/stk-callback/'
#
#             response = cl.stk_push(phone, amount, account_reference, transaction_desc, callback_url)
#
#             # Ensure JSON-parsed response
#             response_data = response.json() if hasattr(response, 'json') else response
#             print(response_data)
#             checkout_id = response_data.get("CheckoutRequestID")
#
#             if checkout_id:
#                 deposit.checkout_request_id = checkout_id
#                 deposit.save()
#
#
#             messages.success(
#                 request,
#                 f"STK Push sent to your phone ({deposit.phone_number}). Please confirm to complete deposit."
#             )
#             print(response.text)
#
#         except Exception as e:
#             messages.error(request, f"Failed to initiate STK Push: {e} : Check your Internet Connection")
#
#         return redirect('deposits:make_deposit')
#
#     # GET request
#     deposit_form = DepositForm()
#
#     context = {
#         'user_deposits': user_deposits,
#         'user_deposits_count': user_deposits.count(),
#         'deposit_form': deposit_form,
#     }
#     return render(request, 'Deposit/deposit.html', context)


@csrf_exempt
@csrf_exempt
def stk_callback(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        mpesa_response = json.loads(request.body)
        print("M-Pesa Callback:", json.dumps(mpesa_response, indent=2))

        callback = mpesa_response.get('Body', {}).get('stkCallback', {})
        result_code = callback.get('ResultCode')
        result_desc = callback.get('ResultDesc', '')

        if result_code == 0:
            metadata_items = callback.get('CallbackMetadata', {}).get('Item', [])
            metadata = {item['Name']: item['Value'] for item in metadata_items if 'Value' in item}

            amount = metadata.get('Amount')
            phone = str(metadata.get('PhoneNumber'))[-9:] if metadata.get('PhoneNumber') else None
            mpesa_code = metadata.get('MpesaReceiptNumber')
            checkout_id = callback.get('CheckoutRequestID')

            if not all([amount, phone, mpesa_code]):
                print("Missing transaction details in callback.")
                return JsonResponse({"ResultCode": 1, "ResultDesc": "Incomplete transaction data."})

            deposit = Deposit.objects.filter(
                phone_number__endswith=phone,
                amount=amount,
                paid=False,
                checkout_request_id=checkout_id
            ).last()

            if deposit:
                deposit.paid = True
                deposit.mpesa_receipt_number = mpesa_code  # Save if field exists
                deposit.save()
                print(f"Deposit confirmed for {deposit.user.username} - {deposit.reference_code}")
            else:
                print(f"No matching deposit found for phone={phone}, amount={amount}, checkout_id={checkout_id}")

        else:
            # Handle failed transaction (e.g. user cancelled, timeout, etc.)
            print(f"Transaction failed: ResultCode={result_code}, Desc={result_desc}")

        return JsonResponse({"ResultCode": 0, "ResultDesc": "Callback received successfully"})

    except Exception as e:
        print("Callback processing error:", e)
        return JsonResponse({"ResultCode": 1, "ResultDesc": f"Callback error: {str(e)}"})


@login_required
def stk_status(request, checkout_id):
    deposit = get_object_or_404(Deposit, checkout_request_id=checkout_id, user=request.user)

    return JsonResponse({
        "reference": deposit.reference_code,
        "status": "paid" if deposit.paid else "pending",
        "amount": deposit.amount,
        "result_desc": "Confirmed" if deposit.paid else "Waiting for confirmation"
    })


# def stk_callback(request):
#     if request.method == 'POST':
#         mpesa_response = json.loads(request.body)
#         print("M-Pesa Callback:", mpesa_response)
#
#         try:
#             callback = mpesa_response['Body']['stkCallback']
#             result_code = callback['ResultCode']
#
#             if result_code == 0:
#                 amount = callback['CallbackMetadata']['Item'][0]['Value']
#                 phone = str(callback['CallbackMetadata']['Item'][4]['Value'])[-9:]  # last 9 digits
#                 mpesa_code = callback['CallbackMetadata']['Item'][1]['Value']  # Mpesa receipt no
#
#                 # Match the most recent unpaid deposit for that phone and amount
#                 deposit = Deposit.objects.filter(phone_number__endswith=phone, amount=amount, paid=False).last()
#                 if deposit:
#                     deposit.paid = True
#                     deposit.save()
#
#                     print(f"Deposit confirmed for {deposit.user.username} - {deposit.reference_code}")
#                 else:
#                     print(f"No matching deposit found for phone: {phone}, amount: {amount}")
#
#             return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})
#
#         except Exception as e:
#             print("Callback processing error:", e)
#             return JsonResponse({"ResultCode": 1, "ResultDesc": f"Failed: {e}"})
#
#     return JsonResponse({"error": "Invalid request"}, status=400)

# @login_required
# def stk_status(request, checkout_id):
#     deposit = get_object_or_404(Deposit, checkout_request_id=checkout_id, user=request.user)
#
#     status = "Paid" if deposit.paid else "Pending"
#     return JsonResponse({
#         "reference": deposit.reference_code,
#         "status": status,
#         "amount": deposit.amount,
#         "result_desc": "Confirmed" if deposit.paid else "Waiting for confirmation"
#     })


# def daraja_stk_push(request):
#     try:
#         cl = MpesaClient()
#         # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
#         phone_number = '0708374149'
#         amount = 100
#         account_reference = 'ZenithAchievers'
#         transaction_desc = 'Description'
#         callback_url = 'http://zenithachievers.com/mpesa/stk-callback/'
#         response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
#         print(response)
#         return HttpResponse(response)
#
#     except Exception as e:
#         messages.error(request, f"An Error Occurred... {e}.")
#         return redirect('deposits:make_deposit')
#

#
# @csrf_exempt
# def stk_callback(request):
#     if request.method == 'POST':
#         mpesa_response = json.loads(request.body)
#         print("M-Pesa Callback:", mpesa_response)
#
#         # You can now save the payment status, phone, transaction code, etc.
#         # Example: result_code = mpesa_response['Body']['stkCallback']['ResultCode']
#
#         return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})
#     return JsonResponse({"error": "Invalid request"}, status=400)

# @login_required
# def stk_status(request, checkout_id):
#     stk = get_object_or_404(StkPushRequest, checkout_request_id=checkout_id, user=request.user)
#     return JsonResponse({"status": stk.status, "result_desc": stk.result_desc})