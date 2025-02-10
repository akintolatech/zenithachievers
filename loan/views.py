from django.shortcuts import render, redirect
from .models import LoanRequest
from .forms import  LoanRequestForm
from django.contrib import messages


# Create your views here.
def make_loan_request(request):
    user_loan_requests = LoanRequest.objects.filter(user=request.user)

    if request.method == "POST":
        loan_request_form = LoanRequestForm(request.POST)
        if loan_request_form.is_valid():
            loan_request = loan_request_form.save(commit=False)
            loan_request.user = request.user
            loan_request.save()
            messages.success(request, "Your Loan Request have been successfully Placed - Your Loan will be available for withdrawal after approved by Admin!")
            return redirect('loan:make_loan_request')

    else:
        loan_request_form = LoanRequestForm()

    context = {
        'user_loan_requests': user_loan_requests,
        'user_loan_requests_count': user_loan_requests.count(),
        "loan_request_form": loan_request_form
    }
    return render(request, 'loan/loan.html', context)