from django.db import models

# Create your models here.
class Shop(models.Model):
    admin_user = models.OneToOneField("accounts.CustomUser", on_delete=models.CASCADE, related_name='shop')
    name = models.CharField(max_length=255)
    code=models.CharField(max_length=10, unique=True, blank=True, null=True)
    slug = models.SlugField(unique=True,blank=True, null=True)
    owner_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    postal_code=models.CharField(max_length=50)
    map_location_url=models.URLField(blank=True, null=True)
    
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to="shop_logos/", blank=True, null=True)
    banner = models.ImageField(upload_to="shop_banners/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    updated_at = models.DateTimeField(auto_now=True)
    established_date = models.DateField(blank=True, null=True)
    
    
    def __str__(self):
        return self.name 
    
class Item(models.Model):
    name=models.CharField(max_length=100)
    shop=models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='items')
    
    
    class Meta:
        unique_together = ('name', 'shop')
        
        
    def __str__(self):
        return f"{self.name} | {self.shop}" 
        
        
class Price(models.Model):
    name=models.CharField(max_length=100)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    item=models.ForeignKey(Item, on_delete=models.CASCADE, related_name='prices')
    
    class Meta:
        unique_together = ('name', 'item')
        
    def __str__(self):
        return f"{self.name} | {self.item}" 