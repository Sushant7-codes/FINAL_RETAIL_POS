from django import forms
from shop.models import Shop
from django.utils.text import slugify

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        exclude = ["admin_user","slug","is_active","updated_at"]
        
        widgets={
            "established_date":forms.DateInput(attrs={"type":"date"}),
        }
        
        
    def __init__(self,*args,**kwargs):
        self.request=kwargs.pop("request") if "request" in kwargs else None
        super().__init__(*args, **kwargs)
    
    
    def save(self,commit=True,*args,**kwargs):
        shop = super(ShopForm, self).save(commit=False, *args, **kwargs)
        
        
        if self.request:
            shop.admin_user =self.request.user
            
        if not shop.code:
            shop_name=self.cleaned_data.get("name")
            shop_name_words=shop_name.split(" ")
            estd_year=self.cleaned_data.get("established_date").year
            code="".join([word[0] for word in shop_name_words])+f"-{estd_year}"
            shop.code=code
            shop.slug= slugify(shop_name)
        
        if commit:
            shop.save()
        
        return shop