from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from shop.forms import ShopForm
# Create your views here.


@require_POST
def shop_register(request):
    form_data=request.POST
    form=ShopForm(form_data, request.FILES)
    
    if form.is_valid():
        form.save(request=request)
        return redirect("app:dashboard")
    
    return render(request, "app/dashboard.html", {"form":form})