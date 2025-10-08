from django import forms
from shop.models import Shop
from django.utils.text import slugify

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        exclude = ["admin_user", "slug", "is_active", "updated_at"]

        widgets = {
            "established_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)  # safely pop request
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        shop = super().save(commit=False)

        # Set admin_user from request
        if self.request:
            shop.admin_user = self.request.user

        # Generate code & slug if not already set
        if not shop.code:
            shop_name = self.cleaned_data.get("name")
            if shop_name:
                shop_name_words = shop_name.split(" ")
                estd_date = self.cleaned_data.get("established_date")
                estd_year = estd_date.year if estd_date else "0000"
                code = "".join([word[0] for word in shop_name_words]) + f"-{estd_year}"
                shop.code = code.upper()[:10]  # keep within max_length
                shop.slug = slugify(shop_name)

        if commit:
            shop.save()
        return shop
from django import forms
from shop.models import Shop
from django.utils.text import slugify

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        exclude = ["admin_user", "slug", "is_active", "updated_at"]

        widgets = {
            "established_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def generate_unique_slug(self, name, instance_id=None):
        """
        Generate a unique slug from name.
        If a slug already exists, append a counter.
        """
        base_slug = slugify(name)
        slug = base_slug
        counter = 1

        # Keep checking until slug is unique
        while Shop.objects.filter(slug=slug).exclude(id=instance_id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def save(self, commit=True):
        shop = super().save(commit=False)

        if self.request:
            shop.admin_user = self.request.user

        # Generate code only if missing
        if not shop.code:
            shop_name = self.cleaned_data.get("name")
            if shop_name:
                words = shop_name.split(" ")
                estd_date = self.cleaned_data.get("established_date")
                estd_year = estd_date.year if estd_date else "0000"
                code = "".join([w[0] for w in words]) + f"-{estd_year}"
                shop.code = code.upper()[:10]

        # Always ensure unique slug (use instance id to allow self-updates)
        if self.cleaned_data.get("name"):
            shop.slug = self.generate_unique_slug(
                self.cleaned_data["name"], instance_id=shop.id
            )

        if commit:
            shop.save()
        return shop
