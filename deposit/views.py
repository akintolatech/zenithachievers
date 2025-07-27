from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Deposit, StkPushRequest
from .forms import DepositForm
from django.contrib import messages

import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .mpesa import lipa_na_mpesa_online


@login_required
def deposit_page(request):
    user_deposits = Deposit.objects.filter(user=request.user)

    if request.method == "POST":
        deposit_form = DepositForm(request.POST)
        if deposit_form.is_valid():
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




@login_required
def initiate_stk_push(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    amount = request.POST.get("amount")
    phone = request.POST.get("phone_number")
    if phone.startswith("0"): phone = "254" + phone[1:]
    if phone.startswith("+"): phone = phone[1:]
    deposit = Deposit.objects.create(user=request.user, amount=amount, paid=False)
    resp = lipa_na_mpesa_online(amount=amount, phone=phone, account_ref=str(request.user.id), description=f"Dep#{deposit.pk}")
    stk = StkPushRequest.objects.create(
        user=request.user,
        amount=amount,
        phone_number=phone,
        merchant_request_id=resp.get("MerchantRequestID", ""),
        checkout_request_id=resp.get("CheckoutRequestID", ""),
        response_code=resp.get("ResponseCode", ""),
        response_description=resp.get("ResponseDescription", ""),
        customer_message=resp.get("CustomerMessage", ""),
        deposit=deposit,
    )
    return JsonResponse({"ok": True, "message": resp.get("CustomerMessage", ""), "checkout_request_id": stk.checkout_request_id})

@csrf_exempt
def stk_callback(request):
    data = json.loads(request.body.decode("utf-8"))
    body = data.get("Body", {}).get("stkCallback", {})
    checkout = body.get("CheckoutRequestID")
    result_code = body.get("ResultCode")
    result_desc = body.get("ResultDesc")
    stk = get_object_or_404(StkPushRequest, checkout_request_id=checkout)
    stk.result_code = str(result_code)
    stk.result_desc = result_desc
    if result_code == 0:
        items = body.get("CallbackMetadata", {}).get("Item", [])
        mpesa_receipt = next((i["Value"] for i in items if i["Name"] == "MpesaReceiptNumber"), "")
        stk.mpesa_receipt = mpesa_receipt
        stk.status = "SUCCESS"
        if stk.deposit:
            stk.deposit.reference_code = mpesa_receipt
            stk.deposit.paid = True
            stk.deposit.save()
    else:
        stk.status = "FAILED"
    stk.save()
    return HttpResponse(status=200)

@login_required
def stk_status(request, checkout_id):
    stk = get_object_or_404(StkPushRequest, checkout_request_id=checkout_id, user=request.user)
    return JsonResponse({"status": stk.status, "result_desc": stk.result_desc})
