
from django import forms
from deposit.models import Deposit
from finance.models import Withdraw
from whatsapp.models import WhatsappScreenshot


class DepositApprovalForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['reference_code', 'amount', 'phone_number', 'paid']
        widgets = {
            # 'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'reference_code': forms.TextInput(attrs={'readonly': 'readonly'}),
            'amount': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'phone_number': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class WithdrawApprovalForm(forms.ModelForm):
    class Meta:
        model = Withdraw
        fields = ['reference_code', 'amount', 'charge', 'approved']
        widgets = {
            # 'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'reference_code': forms.TextInput(attrs={'readonly': 'readonly'}),
            'amount': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'charge': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class WhatsappScreenshotApprovalForm(forms.ModelForm):
    class Meta:
        model = WhatsappScreenshot
        fields = ['screenshot_reference_code', 'number_of_views', 'approved']
        widgets = {
            # 'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'screenshot_reference_code': forms.TextInput(attrs={'readonly': 'readonly'}),
            'number_of_views': forms.NumberInput(),

        }