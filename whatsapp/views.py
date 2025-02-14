from django.shortcuts import render, redirect
from .forms import WhatsappScreenshotForm, WhatsappWithdrawalForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import Profile
from .models import WhatsappWithdrawal, WhatsappScreenshot


@login_required
def submit_whatsapp_screenshot(request):

    user_screenshots = WhatsappScreenshot.objects.filter(user=request.user)

    if request.method == "POST":
        whatsapp_screenshot_form = WhatsappScreenshotForm(request.POST, request.FILES)
        if whatsapp_screenshot_form.is_valid():
            screenshot = whatsapp_screenshot_form.save(commit=False)
            screenshot.user = request.user  # Attach the logged-in user
            screenshot.save()
            messages.success(request, "Screenshot has been successfully submitted for approval!")
            return redirect('whatsapp:submit_whatsapp_screenshot')  # Redirect after success
    else:
        whatsapp_screenshot_form = WhatsappScreenshotForm()

    return render(request, 'whatsapp/whatsapp.html', {'whatsapp_screenshot_form': whatsapp_screenshot_form, "user_screenshots": user_screenshots})


@login_required
def make_whatsapp_withdrawal(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found. Please contact support.")
        return redirect("whatsapp:make_whatsapp_withdrawal")

    if request.method == "POST":
        whatsapp_withdraw_form = WhatsappWithdrawalForm(request.POST)
        if whatsapp_withdraw_form.is_valid():
            withdrawal_amount = whatsapp_withdraw_form.cleaned_data["amount"]

            if withdrawal_amount > profile.whatsapp_earnings or withdrawal_amount == 0:
                messages.error(request, "Insufficient funds for withdrawal.")
                return redirect("whatsapp:make_whatsapp_withdrawal")

            # Proceed with withdrawal
            withdrawal = whatsapp_withdraw_form.save(commit=False)
            withdrawal.user = user
            withdrawal.save()

            messages.success(request, "Whatsapp Withdrawal request submitted successfully.")
            return redirect("whatsapp:make_whatsapp_withdrawal")

    else:
        whatsapp_withdraw_form = WhatsappWithdrawalForm()

    withdrawals = WhatsappWithdrawal.objects.filter(user=user).order_by("-created")

    return render(request, "whatsapp/whatsappwithdrawals.html", {
        "whatsapp_withdraw_form": whatsapp_withdraw_form,
        "withdrawals": withdrawals
    })