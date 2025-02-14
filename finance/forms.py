from django import forms
from .models import Transfer
from django.core.exceptions import ValidationError
from decimal import Decimal

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['receiver', 'amount']

    # # Custom validation for the 'amount' field (e.g., ensure it's positive)
    # def clean_amount(self):
    #     amount = self.cleaned_data.get('amount')
    #     if amount <= 0:
    #         raise ValidationError("Transfer amount must be greater than zero.")
    #     return amount
    #
    # # Custom validation to ensure sender has sufficient balance
    # def clean(self):
    #     cleaned_data = super().clean()
    #     sender = self.instance.sender  # The sender is already assigned when creating the Transfer instance
    #     amount = cleaned_data.get('amount')
    #
    #     if sender.profile.deposit_balance < amount:
    #         raise ValidationError("Insufficient funds for transfer.")
    #
    #     return cleaned_data

    def __init__(self, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
