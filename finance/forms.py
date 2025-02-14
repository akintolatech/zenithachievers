from django import forms
from .models import Transfer, Withdraw
from django.core.exceptions import ValidationError
from decimal import Decimal

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['receiver', 'amount']

    def __init__(self, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdraw
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        super(WithdrawalForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'