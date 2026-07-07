from django.shortcuts import render
from shop.models import Price
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def billing(request):
    if request.user.role == request.user.Roles.SHOP_ADMIN:
        shop = request.user.shop
    else:
        shop = request.user.workplace
        
    items = Price.objects.filter(
        item__shop=shop).select_related("item").order_by("name")
    
    context = {
        "shop": shop,
        "user": request.user,
        "items": items,
    }
    
    items = Price.objects.filter(
    item__shop=shop
    ).select_related("item").order_by("name")

    print("Current Shop:", shop)
    print("Products:", items.count())

    for product in items:
        print(product.name)
    
    return render(request, "billing/billing.html", context)