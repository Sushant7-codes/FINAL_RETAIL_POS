from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.forms import ShopForm

@login_required
def dashboard(request):
    
    try:
        request.user.shop
    except Exception as e:
        print(e)
        message=(
            "Welcome to the dashboard, please create a shop to get started !"
        )
        messages.info(request, message)
        
        shop_res_form = ShopForm()
        context={"form":shop_res_form}
        return render(request, "app/dashboard.html", context)
    
    return render(request, "app/dashboard.html")