from django import forms
from .models import WhatsappScreenshot, WhatsappWithdrawal

class WhatsappScreenshotForm(forms.ModelForm):
    class Meta:
        model = WhatsappScreenshot
        fields = [ 'number_of_views', 'screenshot']

    def clean_screenshot(self):
        screenshot = self.cleaned_data.get('screenshot')
        if screenshot:
            ext = screenshot.name.split('.')[-1].lower()
            if ext not in ['png', 'jpg', 'jpeg']:
                raise forms.ValidationError("Only .png, .jpg, and .jpeg files are allowed.")
        return screenshot

    def __init__(self, *args, **kwargs):
        super(WhatsappScreenshotForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class WhatsappWithdrawalForm(forms.ModelForm):
    class Meta:
        model = WhatsappWithdrawal
        fields = ["amount"]

    def __init__(self, *args, **kwargs):
        super(WhatsappWithdrawalForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'