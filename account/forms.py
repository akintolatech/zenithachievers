from django import forms
from django.contrib.auth import get_user_model
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password',
                # 'maxlength': '7',
                # 'pattern': r'\d{2}/\d{4}'
            }
        )
    )


class UserRegistrationForm(forms.ModelForm):

    # referral_code = forms.CharField(
    #     label='Referral Code (Optional)',
    #     required=False
    # )

    phone_number = forms.CharField(
        label='Phone Number(Mpesa)',
        widget=forms.TextInput
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', ]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email']

        # Add the 'form-control' class to all fields
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Add the 'form-control' class to all fields
            for field_name, field in self.fields.items():
                field.widget.attrs.update({'class': 'form-control'})


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'photo']


