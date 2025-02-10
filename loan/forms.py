from django import forms
from .models import LoanRequest

class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ['amount', 'duration']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        super(LoanRequestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
