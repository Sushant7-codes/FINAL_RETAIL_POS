from django import forms
from shop.models import Shop

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'owner_name', 'email', 'phone_number', 'address', 'registration_number', 'logo', 'banner']