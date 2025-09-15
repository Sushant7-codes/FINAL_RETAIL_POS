from django.db import models

# Create your models here.
class Shop(models.Model):
    admin_user = models.OneToOneField("accounts.CustomUser", on_delete=models.CASCADE, related_name='shop')
    name = models.CharField(max_length=255)
    code=models.CharField(max_length=10, unique=True)
    slug = models.SlugField(unique=True,blank=True, null=True)
    owner_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    
    address = models.CharField(max_length=20)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to="shop_logos/", blank=True, null=True)
    banner = models.ImageField(upload_to="shop_banners/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    established_date = models.DateField(blank=True, null=True)
    
    
    def __str__(self):
        return self.name 