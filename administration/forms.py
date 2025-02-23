from django import forms
# from shop.models import Product
#
#
# class ProductForm(forms.Form):
#     class Meta:
#         model = Product
#         fields = ["category", "name", "image", "description", "price", "available"]
#
# class EditProductForm(forms.Form):
#     class Meta:
#         model = Product
#         fields = ["name", "image" , "description"]

        # Overriding the widget for the 'photo' field to include an id

    # def __init__(self, *args, **kwargs):
    #     super(EditProductForm, self).__init__(*args, **kwargs)
    #     self.fields['image'].widget.attrs.update({'id': 'image_input_id'})


from django import forms
from deposit.models import Deposit

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