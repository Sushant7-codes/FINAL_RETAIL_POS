from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from shop.forms import ShopForm
from shop.models import Shop
from django.contrib.auth.decorators import login_required
# Create your views here.


@require_POST
def shop_register(request):
    form_data=request.POST
    form=ShopForm(form_data, request.FILES)
    
    if form.is_valid():
        form.save(request=request)
        return redirect("shop:shop_profile")
    
    return render(request, "app/dashboard.html", {"form":form})


@require_GET
@login_required
def shop_profile(request):
    
    shop_admin= request.user 
    try:
        shop_data=shop_admin.shop
    except Exception as e:
        print(e)
        return redirect("app:dashboard")
    
    context={
        'admin':shop_admin,
        'shop':shop_data
    }
    
    return render(request, "shop/profile.html",context)


@login_required
def shop_update(request):
    
    if request.method == "POST":
        form_data=request.POST
        form=ShopForm(form_data, request.FILES)
        
        if form.is_valid():
            form.save(request=request)
            return redirect("shop:shop_profile")
        
    form = ShopForm(instance=request.user.shop)
    
    return render(request, "shop/update-shop-info.html", {"form":form})